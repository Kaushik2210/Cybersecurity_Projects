# Day 06 — Notes

## What I learned

Running real Lynis alongside my own 10-check script was the most useful part
of this. Lynis found things I hadn't even thought to check, password
hashing rounds, minimum password age (not just maximum), a PAM module for
password strength, vulnerable installed packages, whether klogd is running.
Seeing that list made it obvious that a "CIS hardening" project with only 10
checks is a real but small slice of the actual standard, not a complete
implementation, and the README says so honestly rather than implying full
coverage.

The hardening index moving from 57 to 59 instead of jumping dramatically was
a good reality check too. It would have been easy to expect a bigger number
given six checks flipped from FAIL to PASS, but Lynis is weighing roughly
229 things, our fixes are a small fraction of its total surface.

## What broke and how I fixed it

- Nothing broke in the scripts themselves on this run, they worked
  correctly on the first try. Copying files into the container hit the same
  Git-Bash-on-Windows path mangling from Day 01, `MSYS_NO_PATHCONV=1` plus
  Windows-style host paths fixed it the same way.
- Needed `--privileged` on the container so it could actually write to
  `/proc/sys/fs/suid_dumpable` and `/proc/sys/net/ipv4/ip_forward`, an
  unprivileged container blocks writes to those paths, which would have
  made the corresponding checks permanently N/A rather than a real
  before/after.

## Interview questions someone could ask me about this
1. Q: Why are checking and hardening kept as two separate scripts?
   A: An audit should carry zero risk of changing anything. Keeping the
   write path separate, requiring root, and backing up every file means
   someone makes a deliberate decision before anything actually changes.

2. Q: The hardening index only moved from 57 to 59. Does that mean the hardening didn't work?
   A: No. The 10 controls fixed here are a narrow slice of what Lynis
   checks overall. `cis_check.sh`'s own before/after (6 failures to 0) is
   the accurate measure of what this specific script did.

3. Q: What's the real risk in a script like this if run carelessly on a remote server?
   A: Setting PermitRootLogin no before confirming a working non-root sudo
   account exists can permanently lock out remote access with no console
   fallback. Test on a disposable VM first, never a remote production
   server.

4. Q: How would you extend this to a fleet of servers instead of one host?
   A: Convert both scripts into an Ansible playbook with idempotent tasks,
   and use its check/diff mode as the audit-only equivalent of
   `cis_check.sh` before applying changes fleet-wide.
