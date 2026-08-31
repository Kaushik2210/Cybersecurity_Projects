# Where these captures came from

All three are official Wireshark project sample/test captures — public,
benign, and widely used for teaching protocol analysis. None of these were
captured on my own network.

- `dns.cap` — from Wireshark's own [Sample Captures wiki
  page](https://wiki.wireshark.org/SampleCaptures). A short mixed-record DNS
  capture (A, AAAA, MX, PTR, SRV lookups).
- `dhcp.pcap` — from the [Wireshark source repository's test
  suite](https://gitlab.com/wireshark/wireshark/-/tree/master/test/captures),
  used by Wireshark's own automated tests. A minimal 4-packet DHCP exchange.
- `http.pcap` — also from the Wireshark test suite. A single plaintext HTTP
  request (a legacy Windows Update check, not something I generated).

Fetched with plain `curl`, no scraping or bulk download involved.
