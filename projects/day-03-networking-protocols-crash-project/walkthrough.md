# Day 03 — Walkthrough

Exact commands, in order, with what to expect at each step.

## Step 1 — See the "normal tool" view first

```bash
dig example.com
```
Expected output: an ANSWER SECTION with `example.com.` mapped to one or more
IP addresses, and a `Query time:` line near the bottom.

```bash
curl -w "\ndns: %{time_namelookup}s connect: %{time_connect}s tls: %{time_appconnect}s ttfb: %{time_starttransfer}s total: %{time_total}s\n" -o /dev/null -s https://example.com
```
Expected output: a line of per-phase timings curl already tracks internally
— this is the same breakdown the Python script produces, but from a tool
whose internals you haven't seen yet.

## Step 2 — Run the phase-by-phase tracer

```bash
python code/http_lifecycle_trace.py example.com
```
Expected output:
```
Tracing https://example.com:443/

[1] DNS resolution:        ~90 ms -> <ip addresses>
[2] TCP connect:           ~30 ms -> <ip>:443
[3] TLS handshake:         ~40 ms -> TLSv1.3, <cipher>
    Certificate subject: example.com
    Certificate issuer:  <CA name>
    Valid until:         <date>
[4] Time to first byte:    ~60 ms -> HTTP/1.1 200 OK

Total (DNS + TCP + TLS + TTFB): ~220 ms
```
Compare this against curl's numbers from Step 1 — they should be in the same
ballpark (the script measures the same phases, just visibly).

## Step 3 — Try the plain-HTTP and failure paths

```bash
python code/http_lifecycle_trace.py example.com --no-tls --port 80
python code/http_lifecycle_trace.py this-domain-should-not-exist-xyz123.invalid
```
Expected output: the first skips phase 3 with `skipped (--no-tls)`; the
second fails at phase 1 with `DNS resolution failed: ...` and exits non-zero
— confirming each phase's errors are caught individually rather than
crashing the whole script.

## Step 4 — Capture the same request in Wireshark

1. Start capturing on your active interface, with a filter to keep the
   capture small:
   ```
   host example.com
   ```
2. In another terminal, re-run:
   ```bash
   python code/http_lifecycle_trace.py example.com
   ```
3. Stop the capture. You should be able to find, in order: the DNS query
   and response, the TCP SYN/SYN-ACK/ACK, the TLS ClientHello (look for the
   SNI extension in its details pane) through Finished, and the HTTP GET and
   200 OK.

<!-- Screenshot placeholder: ![](evidence/01-wireshark-tls-handshake.png) -->

## Step 5 — Save evidence

```bash
mkdir -p evidence
python code/http_lifecycle_trace.py example.com > evidence/trace-output.txt
```
Save the Wireshark capture as `evidence/https-request.pcapng` (File → Save
As). Review both files before committing — they'll only contain traffic to
a public site, but confirm nothing else was running during the capture.
