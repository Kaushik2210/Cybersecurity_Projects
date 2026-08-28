# Day 01 — Notes

## What I learned
<!-- Fill in after doing the hands-on lab: what clicked, what the segmentation
     actually looked like once it was real instead of theoretical. -->

## What broke and how I fixed it
<!-- Fill in as you hit real issues — e.g. forgot to enable IP forwarding,
     internal network name typo caused two VMs to silently not connect, etc. -->

## Interview questions someone could ask me about this
1. Q: Why test segmentation from inside each segment instead of from one central scanner?
   A: Reachability depends on the vantage point relative to the firewall/VLAN
   rule. A scanner outside the rule's path can't tell you whether the rule
   itself works — only whether the scanner itself can reach the target.

2. Q: What's "deny by default" and why does it matter here?
   A: Every cross-segment path is assumed blocked unless explicitly declared
   in `allowed_paths`. That means a new, accidental path shows up as a policy
   violation automatically, instead of silently working until someone notices.

3. Q: What would make this segmentation setup a false sense of security?
   A: If the router VM's own OS-level packet forwarding isn't actually locked
   down (e.g. a permissive default forward policy) and only the GUI-level
   rules are restrictive, an attacker with router access bypasses the whole
   model.

4. Q: How does this connect to a real breach?
   A: Most large-scale lateral movement (e.g. ransomware spreading from one
   workstation to a file server) succeeds because internal networks are flat.
   Segmentation with a verified deny-by-default policy is the control that
   turns "one machine popped" into "one machine popped, contained."
