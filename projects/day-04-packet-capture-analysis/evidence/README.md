# Evidence — Day 04

Real output from running `code/pcap_summary.py` against all three sample
captures (see `code/samples/SOURCES.md` for where they came from):

- `summary-dns.cap.txt` — 38 packets, all UDP, real DNS query variety (A,
  AAAA, MX, PTR, SRV, and one typo-looking domain worth flagging).
- `summary-dhcp.pcap.txt` — a minimal 4-packet DHCP exchange.
- `summary-http.pcap.txt` — a single packet, but a real plaintext HTTP
  request to `windowsupdate.microsoft.com`.

## Still to add

The manual Wireshark side of `walkthrough.md` (Statistics → Protocol
Hierarchy, Conversations, DNS filter) and screenshots of that, to sit
alongside this scripted output. The stretch-goal malware pcap analysis is
also still pending and will get its own subfolder here once done, in an
isolated VM per malware-traffic-analysis.net's own handling guidance.
