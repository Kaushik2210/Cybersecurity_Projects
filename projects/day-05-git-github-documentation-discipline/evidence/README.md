# Evidence — Day 05

Real output from `repo_audit.py` against this actual repo, before and after
Day 05's own docs existed:

- `structure-audit-before.txt` — run while this project's README, walkthrough,
  and notes didn't exist yet. Correctly flagged Day 05 as FAIL, 0/3 required
  files.
- `structure-audit-after.txt` — same command, run once those files were
  written. Clean PASS across all 5 days, 0 total issues.
- `commits-audit.txt` — the commit-style check against this repo's real git
  history, run after fixing the `%s`/`%b` vs `%B` bug described in
  `notes.md`. All 8 commits at the time came back clean.

No fabricated "before" state here, the before-run genuinely happened first;
the folder just didn't have its own files yet when it was written.
