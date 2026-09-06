# Evidence — Day 06

All real output from a `debian:12-slim` Docker container (run
`--privileged` so it could actually write to `/proc/sys`), not the full VM
lab from the walkthrough, which is still pending.

- `cis-check-before.txt` — the real 10-check audit on a fresh container: 4
  passed, 6 failed.
- `cis-harden-output.txt` — real output from running `cis_harden.sh` as
  root: every fix it applied, and confirmation each touched file was
  backed up first.
- `cis-check-after.txt` — the same audit, same container, after hardening:
  10 passed, 0 failed.
- `lynis-report-before.dat` — Lynis' full structured report from a
  separate, freshly-installed baseline container (hardening_index=57).
- `lynis-report-after.dat` — Lynis' report from the hardened container
  (hardening_index=59).
- `lynis-audit-full.txt` — the full terminal output of the after-hardening
  Lynis run, ANSI color codes stripped for readability.

## What this does and doesn't prove

The Lynis before/after used two separate fresh containers (one hardened,
one not), not the same container audited twice, so the 57 -> 59 delta is a
genuine independent comparison, not Lynis re-scoring its own prior state.
Lynis checks roughly 229 things; the 10 controls in `cis_check.sh` are a
real but small subset, which is exactly why the index moved by 2 points
instead of dramatically, most of what Lynis flags (password hashing
rounds, minimum password age, vulnerable packages, unused kernel modules)
was never in scope for this project's own script.

## Still to add

Running the same checker/hardener pair on a real VM instead of a container
would surface a few checks this container setup can't fully exercise
(systemd service hardening, `/tmp` on a separate partition), both of which
show up as Lynis suggestions already.
