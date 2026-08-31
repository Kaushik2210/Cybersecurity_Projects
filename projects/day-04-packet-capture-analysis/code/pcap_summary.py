#!/usr/bin/env python3
"""
pcap_summary.py — turn a raw .pcap file into the kind of summary you'd
normally build by clicking through Wireshark's Statistics menus by hand:
protocol breakdown, top talkers, every DNS query seen, and any plaintext
HTTP requests.

WHY BUILD THIS INSTEAD OF JUST USING WIRESHARK
  Wireshark is the right tool for actually reading traffic interactively —
  this doesn't replace that (see walkthrough.md for the Wireshark side of
  Day 04). What this does is turn "I looked through it in Wireshark" into a
  repeatable report you can diff between captures or attach to a writeup,
  and forces you to understand what each summary actually means by
  implementing it yourself: a "top talker" isn't magic, it's just counting
  bytes per (src, dst) pair.

WHAT IT USES
  dpkt — a pure-Python pcap/protocol parsing library. Chosen over scapy for
  this project specifically because it has no dependency on a live packet
  capture driver (Npcap/libpcap); it only ever reads bytes out of an
  existing .pcap file, which is all offline analysis needs.

SAFETY
  Read-only. This never sends a packet — it only parses files already on
  disk.

USAGE
  python pcap_summary.py samples/dns.cap
"""

import argparse
import socket
import struct
import sys
from collections import Counter
from pathlib import Path

import dpkt


def ip_to_str(raw_ip: bytes) -> str:
    """Render a raw 4-byte IPv4 address as dotted-decimal, e.g. '8.8.8.8'."""
    return socket.inet_ntoa(raw_ip)


def protocol_name(ip_proto: int) -> str:
    """Map an IP protocol number to a readable name for the common cases."""
    return {1: "ICMP", 6: "TCP", 17: "UDP"}.get(ip_proto, f"proto-{ip_proto}")


def summarize(pcap_path: Path) -> None:
    packet_count = 0
    first_ts = None
    last_ts = None
    protocol_counts = Counter()
    bytes_per_pair = Counter()          # (src, dst) -> total bytes
    packets_per_pair = Counter()        # (src, dst) -> packet count
    dns_queries = []                    # (qname, qtype) seen in DNS questions
    http_requests = []                  # (host, path) seen in plaintext HTTP

    with pcap_path.open("rb") as f:
        reader = dpkt.pcap.Reader(f)
        for timestamp, raw_packet in reader:
            packet_count += 1
            first_ts = timestamp if first_ts is None else min(first_ts, timestamp)
            last_ts = timestamp if last_ts is None else max(last_ts, timestamp)

            try:
                eth = dpkt.ethernet.Ethernet(raw_packet)
            except dpkt.dpkt.UnpackError:
                continue  # not a well-formed Ethernet frame — skip, don't crash

            if not isinstance(eth.data, dpkt.ip.IP):
                continue  # only IPv4 is handled here, on purpose — keeps the
                          # script small and readable for a Day 04 project

            ip = eth.data
            src = ip_to_str(ip.src)
            dst = ip_to_str(ip.dst)
            proto = protocol_name(ip.p)

            protocol_counts[proto] += 1
            pair = (src, dst)
            bytes_per_pair[pair] += len(raw_packet)
            packets_per_pair[pair] += 1

            # --- DNS: queries travel inside UDP, usually to/from port 53 ---
            if isinstance(ip.data, dpkt.udp.UDP) and (ip.data.sport == 53 or ip.data.dport == 53):
                try:
                    dns = dpkt.dns.DNS(ip.data.data)
                    for question in dns.qd:
                        qtype = {1: "A", 28: "AAAA", 5: "CNAME", 15: "MX"}.get(
                            question.type, f"type-{question.type}"
                        )
                        # dpkt gives back str here, not bytes, but that's a
                        # version-specific detail worth guarding rather than
                        # trusting — handle both so this doesn't break again
                        # on a different dpkt release.
                        name = question.name
                        if isinstance(name, bytes):
                            name = name.decode(errors="replace")
                        dns_queries.append((name, qtype))
                except (dpkt.dpkt.UnpackError, IndexError):
                    pass  # malformed/truncated DNS payload — skip this one packet

            # --- HTTP: plaintext requests travel inside TCP, usually port 80 ---
            if isinstance(ip.data, dpkt.tcp.TCP) and (ip.data.sport == 80 or ip.data.dport == 80):
                try:
                    http = dpkt.http.Request(ip.data.data)
                    host = http.headers.get("host", "?")
                    http_requests.append((host, http.uri))
                except (dpkt.dpkt.UnpackError, dpkt.dpkt.NeedData):
                    pass  # not every TCP/80 packet is a full HTTP request
                          # (most are just TCP ACKs or partial segments)

    # --- Report -----------------------------------------------------------
    print(f"Summary of {pcap_path.name}")
    print(f"  Packets:  {packet_count}")
    if first_ts and last_ts:
        print(f"  Duration: {last_ts - first_ts:.3f}s")

    print("\nProtocol breakdown:")
    for proto, count in protocol_counts.most_common():
        print(f"  {proto:<10} {count}")

    print("\nTop talkers (by bytes, src -> dst):")
    for (src, dst), total_bytes in bytes_per_pair.most_common(5):
        packets = packets_per_pair[(src, dst)]
        print(f"  {src:<16} -> {dst:<16} {total_bytes:>7} bytes over {packets} packets")

    if dns_queries:
        print("\nDNS queries seen:")
        for name, qtype in dns_queries:
            print(f"  {qtype:<6} {name}")

    if http_requests:
        print("\nPlaintext HTTP requests seen:")
        for host, uri in http_requests:
            print(f"  {host}{uri}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pcap_file", type=Path, help="Path to a .pcap file")
    args = parser.parse_args()

    if not args.pcap_file.is_file():
        print(f"File not found: {args.pcap_file}")
        return 1

    summarize(args.pcap_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
