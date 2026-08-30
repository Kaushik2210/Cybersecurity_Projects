# Day 01 — Notes

## What I learned

Before spinning up the actual VirtualBox lab, I ran the checker against
Docker networks instead, mostly to catch bugs cheaply. It turned out to be a
useful exercise on its own: Docker bridge networks only enforce isolation at
the network-membership level, not per port. Two containers on the same
bridge can hit each other on any port, no firewall in between. That's not
how the real pfSense/nftables setup in the walkthrough works, where the rule
is deliberately port-specific (users to dmz on 443 only). It's a good
reminder that "the tool passed" only means as much as the environment it ran
against — the Docker demo proves the *script* works, not that the real
segmentation design does.

## What broke and how I fixed it

- First real run failed with a Python traceback, not a graceful error:
  `ping` isn't installed in the `python:3.13-slim` image by default. Not a
  bug in the script (it's supposed to fail loudly on a missing binary rather
  than silently report "blocked"), but it meant installing `iputils-ping`
  before the check could run to completion.
- Copying files into containers from Git Bash on Windows kept mangling paths
  — `/segmentation_check.py` would get rewritten into a Windows path before
  Docker ever saw it. Fixed by using Windows-style forward-slash paths for
  anything on the host side and `MSYS_NO_PATHCONV=1` for anything meant to
  stay a literal Linux path inside the container.

## Interview questions someone could ask me about this
1. Q: Why test segmentation from inside each segment instead of from one central scanner?
   A: Reachability depends on the vantage point relative to the firewall/VLAN
   rule. A scanner outside the rule's path can only tell you whether it can
   reach the target, which may say nothing about the actual boundary.

2. Q: What's "deny by default" and why does it matter here?
   A: Every cross-segment path is assumed blocked unless explicitly declared
   in `allowed_paths`. A new, accidental path shows up as a policy violation
   automatically instead of silently working until someone notices.

3. Q: What would make this segmentation setup a false sense of security?
   A: If the router VM's own packet forwarding isn't actually locked down
   and only GUI-level rules are restrictive, an attacker with router access
   bypasses the whole model. The Docker demo has a version of this same gap:
   it only proves network-level isolation, not the port-level rule the real
   design needs.

4. Q: How does this connect to a real breach?
   A: Most large-scale lateral movement, ransomware spreading from one
   workstation to a file server, succeeds because internal networks are
   flat. Segmentation with a verified deny-by-default policy is what turns
   "one machine popped" into "one machine popped, contained."
