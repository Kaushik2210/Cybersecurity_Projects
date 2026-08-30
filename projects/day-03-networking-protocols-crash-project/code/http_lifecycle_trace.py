#!/usr/bin/env python3
"""
http_lifecycle_trace.py — time and inspect every phase of a single HTTPS
request, using only Python's standard library so nothing is hidden behind a
library like `requests`.

WHY BUILD THIS INSTEAD OF USING curl -w
  curl's timing flags are useful once you already know what DNS lookup, TCP
  handshake, and TLS handshake actually are. Building this by hand forces you
  to touch each layer directly: resolve a name, open a raw socket, wrap it in
  TLS, write the HTTP request bytes yourself. That's the point of this
  project — not to replace curl, but to stop treating it as a black box.

WHAT IT MEASURES, IN ORDER
  1. DNS resolution      — hostname -> IP address(es)
  2. TCP connect         — the three-way handshake to the chosen IP
  3. TLS handshake       — negotiating the encrypted channel (skipped for
                            plain HTTP targets)
  4. Time to first byte  — from sending the HTTP request to the first byte
                            of the response

SAFETY
  This makes exactly one outbound HTTP(S) request, identical in effect to
  opening the URL in a browser or running `curl`. It does not scan, brute
  force, or send more than one request per run.

USAGE
  python http_lifecycle_trace.py example.com
  python http_lifecycle_trace.py example.com --port 443 --path /
  python http_lifecycle_trace.py example.com --no-tls --port 80
"""

import argparse
import socket
import ssl
import sys
import time


def resolve_dns(hostname: str) -> tuple[list[str], float]:
    """Resolve `hostname` to IP addresses; return (addresses, seconds_taken).

    getaddrinfo is used directly (rather than the older gethostbyname) because
    it's what modern networking code actually uses under the hood — it can
    return both IPv4 and IPv6 results and handles IPv6-only DNS records.
    """
    start = time.perf_counter()
    results = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    elapsed = time.perf_counter() - start
    # getaddrinfo returns one entry per (address family, socktype, ...) combo;
    # de-duplicate down to just the IP strings for a readable report.
    addresses = sorted({r[4][0] for r in results})
    return addresses, elapsed


def tcp_connect(ip_address: str, port: int, timeout: float) -> tuple[socket.socket, float]:
    """Open a TCP connection; return (connected_socket, seconds_taken)."""
    start = time.perf_counter()
    sock = socket.create_connection((ip_address, port), timeout=timeout)
    elapsed = time.perf_counter() - start
    return sock, elapsed


def tls_handshake(sock: socket.socket, hostname: str) -> tuple[ssl.SSLSocket, float, dict]:
    """Wrap `sock` in TLS; return (tls_socket, seconds_taken, cert_info).

    Uses the system's default trust store (create_default_context) rather
    than disabling verification — a security-education project should not
    teach turning off certificate checking as the normal path.
    """
    context = ssl.create_default_context()
    start = time.perf_counter()
    # server_hostname enables SNI (Server Name Indication) — the mechanism
    # that lets one IP host many different HTTPS sites, each with its own
    # certificate, and tells the server which cert to present.
    tls_sock = context.wrap_socket(sock, server_hostname=hostname)
    elapsed = time.perf_counter() - start

    cert = tls_sock.getpeercert()
    cert_info = {
        "tls_version": tls_sock.version(),
        "cipher": tls_sock.cipher()[0] if tls_sock.cipher() else "unknown",
        "subject": dict(x[0] for x in cert.get("subject", [])) if cert else {},
        "issuer": dict(x[0] for x in cert.get("issuer", [])) if cert else {},
        "not_after": cert.get("notAfter") if cert else None,
    }
    return tls_sock, elapsed, cert_info


def send_request_and_time_first_byte(sock, hostname: str, path: str) -> tuple[bytes, float]:
    """Send a minimal HTTP/1.1 GET; return (first_chunk, seconds_to_first_byte)."""
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {hostname}\r\n"
        f"Connection: close\r\n"
        f"User-Agent: cyber-100-day03-lifecycle-trace/1.0\r\n"
        f"\r\n"
    ).encode("ascii")

    start = time.perf_counter()
    sock.sendall(request)
    first_chunk = sock.recv(4096)
    elapsed = time.perf_counter() - start
    return first_chunk, elapsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hostname", help="Target hostname, e.g. example.com")
    parser.add_argument("--port", type=int, default=None, help="Default: 443 (TLS) or 80 (--no-tls)")
    parser.add_argument("--path", default="/", help="Request path (default: /)")
    parser.add_argument("--no-tls", action="store_true", help="Use plain HTTP instead of HTTPS")
    parser.add_argument("--timeout", type=float, default=5.0, help="Per-phase timeout in seconds")
    args = parser.parse_args()

    port = args.port or (80 if args.no_tls else 443)

    print(f"Tracing {'http' if args.no_tls else 'https'}://{args.hostname}:{port}{args.path}\n")

    # --- Phase 1: DNS -------------------------------------------------------
    try:
        addresses, dns_seconds = resolve_dns(args.hostname)
    except socket.gaierror as exc:
        print(f"DNS resolution failed: {exc}")
        return 1
    print(f"[1] DNS resolution:     {dns_seconds*1000:7.1f} ms -> {', '.join(addresses)}")
    target_ip = addresses[0]

    # --- Phase 2: TCP --------------------------------------------------------
    try:
        sock, tcp_seconds = tcp_connect(target_ip, port, args.timeout)
    except OSError as exc:
        print(f"TCP connect to {target_ip}:{port} failed: {exc}")
        return 1
    print(f"[2] TCP connect:        {tcp_seconds*1000:7.1f} ms -> {target_ip}:{port}")

    # --- Phase 3: TLS (skipped for --no-tls) ---------------------------------
    active_socket = sock
    if not args.no_tls:
        try:
            active_socket, tls_seconds, cert_info = tls_handshake(sock, args.hostname)
        except ssl.SSLError as exc:
            print(f"TLS handshake failed: {exc}")
            sock.close()
            return 1
        print(f"[3] TLS handshake:      {tls_seconds*1000:7.1f} ms -> {cert_info['tls_version']}, {cert_info['cipher']}")
        print(f"    Certificate subject: {cert_info['subject'].get('commonName', '?')}")
        print(f"    Certificate issuer:  {cert_info['issuer'].get('commonName', '?')}")
        print(f"    Valid until:         {cert_info['not_after']}")
    else:
        print("[3] TLS handshake:      skipped (--no-tls)")

    # --- Phase 4: HTTP request / time to first byte --------------------------
    try:
        first_chunk, ttfb_seconds = send_request_and_time_first_byte(
            active_socket, args.hostname, args.path
        )
    except OSError as exc:
        print(f"HTTP request failed: {exc}")
        return 1
    status_line = first_chunk.split(b"\r\n", 1)[0].decode("ascii", errors="replace")
    print(f"[4] Time to first byte: {ttfb_seconds*1000:7.1f} ms -> {status_line}")

    active_socket.close()

    total = dns_seconds + tcp_seconds + (tls_seconds if not args.no_tls else 0) + ttfb_seconds
    print(f"\nTotal (DNS + TCP + TLS + TTFB): {total*1000:.1f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
