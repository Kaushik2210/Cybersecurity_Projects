# Day 04 — Walkthrough

Exact commands, in order, with what to expect at each step.

## Step 1 — Open a sample in Wireshark and read it by hand first

Open `code/samples/dns.cap` in Wireshark. Before running any script:

1. **Statistics → Protocol Hierarchy** — note the protocol breakdown.
   Expected: this capture is entirely UDP (DNS runs over UDP by default).
2. **Statistics → Conversations → IPv4 tab, sort by Bytes** — note the top
   talker pair.
3. **Statistics → DNS** (or just filter `dns` and read the packet list) —
   note the query names and types.

Write these down before moving to Step 2 — that's the manual baseline the
script's output gets checked against.

<!-- Screenshot placeholder: ![](evidence/01-wireshark-protocol-hierarchy.png) -->

## Step 2 — Run the script against the same capture

```bash
python code/pcap_summary.py code/samples/dns.cap
```
Expected output: a report with packet count, duration, protocol breakdown,
top 5 talkers by bytes, and every DNS query seen, matching what you found
by hand in Step 1.

## Step 3 — Repeat for the other two samples

```bash
python code/pcap_summary.py code/samples/dhcp.pcap
python code/pcap_summary.py code/samples/http.pcap
```
Expected output: `dhcp.pcap` shows a 4-packet UDP exchange between a client
and `255.255.255.255` (DHCP broadcast); `http.pcap` shows a single TCP
packet and one plaintext HTTP request line under "Plaintext HTTP requests
seen".

## Step 4 — Try the error path

```bash
python code/pcap_summary.py code/samples/does-not-exist.pcap
```
Expected output: `File not found: code/samples/does-not-exist.pcap` and a
non-zero exit code, not a stack trace.

## Step 5 — Save evidence

```bash
mkdir -p evidence
python code/pcap_summary.py code/samples/dns.cap > evidence/summary-dns.cap.txt
python code/pcap_summary.py code/samples/dhcp.pcap > evidence/summary-dhcp.pcap.txt
python code/pcap_summary.py code/samples/http.pcap > evidence/summary-http.pcap.txt
```
Add your Wireshark screenshots from Step 1 alongside these, plus your
handwritten (or typed) notes on what you found manually, so the evidence
folder shows both the manual and scripted analysis side by side.

## Step 6 — Try the stretch goal (optional)

Get a real malicious pcap from
[malware-traffic-analysis.net](https://www.malware-traffic-analysis.net/)
(read their usage guidance first, samples are password-protected zips by
design, to stop antivirus/browsers from touching them automatically). Open
it only in an isolated VM, never on your host machine, and use both
Wireshark and `pcap_summary.py` to build a chronological incident timeline:
first contact, DNS lookups, any C2 traffic, in order.
