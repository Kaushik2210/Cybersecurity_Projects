# Day 04 — Notes

## What I learned

The dns.cap sample turned out to be more interesting than I expected for
something described as a basic sample capture. It has a typo-looking domain
in it (`www.example.notginh`) sitting right next to totally normal lookups
for `www.netbsd.org` and `google.com`. That's a good reminder that even a
"boring" capture can have something worth a second look in it. It also has
real Active Directory-style `_ldap._tcp` SRV lookups, which was a nice
unplanned preview of Day 24-25's AD material.

## What broke and how I fixed it

- First run crashed on the DNS-parsing path: I assumed `dpkt`'s
  `question.name` would be raw `bytes` (matching some documentation and
  older examples I'd seen), and called `.decode()` on it. In the installed
  version it's already a `str`. Fixed by checking the type before deciding
  whether to decode, and left a comment explaining why, since it's the kind
  of thing that could easily break again on a different dpkt version.
- Tried `scapy` first since it's the more commonly recommended library, but
  it couldn't identify these captures' link-layer type correctly without
  Npcap installed, even for pure offline file reading. Switched to `dpkt`,
  which doesn't have that dependency at all, and it read all three files
  correctly on the first try.

## Interview questions someone could ask me about this
1. Q: What's the difference between reading a capture in Wireshark and writing a script to summarize it?
   A: Wireshark is better for open-ended, interactive investigation. A
   script is better for a repeatable, comparable summary, and writing one
   forces understanding exactly how each statistic is computed instead of
   trusting a GUI panel.

2. Q: Why does the script only handle IPv4?
   A: Deliberate scope control. IPv6 needs a second parsing path for
   addresses and extension headers; skipping non-IPv4 packets cleanly is an
   honestly-documented limitation rather than a silent gap.

3. Q: What would make a DNS query in a capture suspicious?
   A: A newly-registered or lookalike domain, like the typo-domain that
   actually showed up in this sample capture, an unusual volume of queries
   to one domain, or encoded-looking subdomains (a common DNS-tunneling
   pattern).

4. Q: Why catch parsing errors per packet instead of around the whole file?
   A: Real captures often have a handful of malformed or truncated packets.
   Catching errors per packet means one bad packet gets skipped, not the
   whole report.
