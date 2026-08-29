# Day 02 — Notes

## What I learned
<!-- Fill in after running this on your real VM: what was actually listening
     that you didn't expect, what your sudoers list really looked like, etc. -->

## What broke and how I fixed it
<!-- Fill in as you hit real issues — e.g. `ss` not installed on a minimal
     image, `lastb` empty because /var/log/btmp doesn't exist yet, etc. -->

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
   A: Run it on a schedule, store each report, and diff consecutive runs —
   new listening ports, new sudoers, or new SUID binaries are the real
   signal, not any single snapshot.
