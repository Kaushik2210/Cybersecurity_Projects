# Day 02 — Notes

## What I learned

Running this against a fresh Debian container instead of a VM with real
usage history made one thing obvious: a baseline report is only as
interesting as the box it's run against. A brand-new container has almost
nothing in "recent logins" and no failed-login history at all, so those
sections came back nearly empty. That's not a bug, it's accurate, but it did
mean the more interesting parts of the report ended up being the SUID
binary list and the sudo group membership, both of which were genuinely
useful to see laid out in one place rather than checked with three separate
commands.

## What broke and how I fixed it

- `systemctl` isn't present in the container at all, since it doesn't run
  systemd. The script's fallback message handled this correctly on the
  first try, which was a good sign that `run_or_note()`-style graceful
  failure is actually doing its job rather than just looking correct on
  paper.
- Needed to actually create a non-root sudoer and a cron job by hand before
  running the script, otherwise the "users with sudo" and "system-wide cron
  jobs" sections would have had nothing real to show.

## Interview questions someone could ask me about this
1. Q: Why avoid `set -e` in this script when it's usually recommended for bash?
   A: Several commands here fail legitimately on some systems (no crontab
   set, no `wheel` group on Debian-family distros). `set -e` would abort the
   whole report on the first one; `run_or_note()` catches and explains the
   failure instead, so the report always finishes.

2. Q: What's the security significance of a SUID bit?
   A: The binary runs with the file owner's privilege (often root), not the
   caller's. A bug in — or an unexpected — SUID binary is a direct path from
   a low-privilege shell to root.

3. Q: Why check root status instead of just requiring root to run the script?
   A: Silently requiring root hides a useful signal: knowing exactly which
   sections need elevation (and documenting that) is part of understanding
   the box's actual privilege boundaries.

4. Q: How would this become an ongoing detection instead of a one-off report?
   A: Run it on a schedule, store each report, and diff consecutive runs.
   New listening ports, new sudoers, or new SUID binaries between two runs
   are the actual signal, not any single snapshot.
