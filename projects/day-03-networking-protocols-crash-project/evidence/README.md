# Evidence — Day 03

## What's actually in here

This one didn't need a VM or a container — the tool makes ordinary outbound
HTTP(S) requests, same as a browser, so it runs the same anywhere with
internet access. Everything here is a real run against `example.com` from
my actual dev machine (Windows, so `nslookup` stands in for `dig`, which
isn't installed there — the Kali/Ubuntu lab VM has `dig` and gets used for
the real walkthrough comparison).

- `trace-https-example.com.txt` — the full four-phase trace: real DNS
  answer, real TCP connect time, a genuine TLS 1.3 handshake with
  `example.com`'s actual certificate (issuer, subject, expiry), and a real
  200 OK.
- `trace-http-example.com.txt` — same target over plain HTTP, `--no-tls`,
  showing the TLS phase correctly skipped.
- `trace-dns-failure.txt` — a deliberately bad hostname, showing the script
  fails cleanly at the DNS phase instead of throwing a stack trace.
- `nslookup-example.com.txt` — the "normal tool" DNS answer for comparison.
- `curl-timings-example.com.txt` — curl's own built-in phase timings for the
  same site, to sanity-check the script's numbers against a tool that's
  already trusted.

## Still to add

The Wireshark capture from `walkthrough.md` Step 4 — that needs to be done
on the Kali VM where Wireshark and `dig` both live, alongside a `dig`-based
run to replace the `nslookup` stand-in.
