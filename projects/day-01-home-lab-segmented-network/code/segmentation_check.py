#!/usr/bin/env python3
"""
segmentation_check.py — prove (or disprove) that your lab's network segments
are actually isolated from each other, the way they're supposed to be.

WHAT THIS DOES
  1. Reads a YAML file describing which hosts belong to which network segment,
     and which cross-segment paths are deliberately allowed (segments.example.yaml
     is the template — copy it to segments.local.yaml and edit).
  2. You copy this script onto ONE host inside each segment and run it there
     with --from-segment <that segment's name>. It then checks reachability
     from THIS host to every host in every OTHER segment (ICMP ping, plus a
     TCP connect for any port declared in allowed_paths).
  3. Compares what it found against what "should" be true:
       - a target with NO matching allowed_paths entry should be UNREACHABLE
       - a target WITH a matching allowed_paths entry should be REACHABLE
         on that specific port
  4. Prints a pass/fail table and exits non-zero if anything violates the
     expected policy — so this can also be wired into a script/cron job later.

IMPORTANT: run this FROM INSIDE each segment, not from your host machine
  Reachability is only meaningful from the vantage point of a host that's
  actually behind the firewall/VLAN rule you're testing. Running this from
  your laptop (which may be on neither segment, or bridged past the rules
  entirely) proves nothing about whether segment A can reach segment B — it
  only proves whether YOUR machine can reach them. Copy this file (and
  segments.local.yaml) onto a VM in each segment, e.g. with `scp`, and run it
  there.

WHY PING + TCP CONNECT (not something fancier)
  Ping (ICMP) proves basic network-layer reachability — the thing VLANs/
  firewall rules are usually built to block first. A raw TCP connect proves
  reachability at a specific port without needing the target service to send
  back any real data. Both are safe, read-only checks against your own hosts.

USAGE
  python segmentation_check.py segments.local.yaml --from-segment users
"""

import socket
import subprocess
import sys
from pathlib import Path

import yaml


def ping_host(host: str, timeout_seconds: int = 2) -> bool:
    """Return True if `host` responds to a single ICMP ping.

    Uses subprocess with an argument LIST (never shell=True, never string
    concatenation) so a malicious/malformed hostname in the config can't be
    interpreted as a shell command.
    """
    # Windows' ping uses -n/-w(ms); everything else (Linux/macOS) uses -c/-W(s).
    if sys.platform.startswith("win"):
        command = ["ping", "-n", "1", "-w", str(timeout_seconds * 1000), host]
    else:
        command = ["ping", "-c", "1", "-W", str(timeout_seconds), host]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=timeout_seconds + 2,
    )
    return result.returncode == 0


def tcp_connect(host: str, port: int, timeout_seconds: int = 2) -> bool:
    """Return True if a TCP connection to host:port succeeds."""
    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return True
    except OSError:
        return False


def load_topology(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_allowed_path(allowed_paths: list, from_segment: str, to_segment: str):
    """Return the allowed_paths entry matching this segment pair, or None."""
    for path in allowed_paths:
        if path["from"] == from_segment and path["to"] == to_segment:
            return path
    return None


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[2] != "--from-segment":
        print(f"Usage: {sys.argv[0]} <path-to-segments-yaml> --from-segment <segment-name>")
        return 2

    config_path = Path(sys.argv[1])
    from_segment = sys.argv[3]

    if not config_path.is_file():
        print(f"Config file not found: {config_path}")
        return 2

    topology = load_topology(config_path)
    segments: dict = topology.get("segments", {})
    allowed_paths: list = topology.get("allowed_paths", [])

    if from_segment not in segments:
        print(f"Unknown segment '{from_segment}'. Known segments: {list(segments.keys())}")
        return 2

    violations = []
    checks_run = 0

    print(f"Running from segment: {from_segment}")
    print(f"{'TO':<10} {'HOST':<16} {'EXPECTED':<14} {'ACTUAL':<14} RESULT")
    print("-" * 66)

    for to_segment, to_info in segments.items():
        if to_segment == from_segment:
            continue  # only cross-segment reachability is interesting here

        allowed = find_allowed_path(allowed_paths, from_segment, to_segment)

        for target_host in to_info["hosts"]:
            checks_run += 1

            if allowed:
                expected = f"reachable:{allowed['port']}"
                actual_ok = tcp_connect(target_host, allowed["port"])
                actual = f"reachable:{allowed['port']}" if actual_ok else "blocked"
            else:
                expected = "blocked"
                actual_ok = ping_host(target_host)
                actual = "reachable" if actual_ok else "blocked"

            expected_ok = expected == actual
            status = "PASS" if expected_ok else "FAIL"

            print(f"{to_segment:<10} {target_host:<16} {expected:<14} {actual:<14} {status}")

            if not expected_ok:
                violations.append(
                    f"{from_segment} -> {to_segment} ({target_host}): "
                    f"expected {expected}, got {actual}"
                )

    print("-" * 66)
    print(f"{checks_run} checks run, {len(violations)} violation(s).")

    if violations:
        print("\nSegmentation policy violations:")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("\nAll cross-segment traffic from this segment matches the declared policy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
