# Day 05 — Walkthrough

Exact commands, in order, with what to expect at each step.

## Step 1 — Run the structure audit

```bash
python code/repo_audit.py structure --repo-root ../../..
```
Expected output: a table of every `projects/day-NN-*/` folder with file,
directory, and section counts, PASS or FAIL per day, and a total issue count
at the bottom. Any FAIL lists exactly what's missing.

## Step 2 — Run the commit-style audit

```bash
python code/repo_audit.py commits --repo-root ../../..
```
Expected output: one line per commit with subject length and either "clean"
or a list of issues (over 72 characters, ends with a period, no blank line
before the body).

## Step 3 — Fix what's flagged

If `structure` reports missing files for a day, that's the actual work: add
the missing README/walkthrough/notes, or the missing `code/`/`evidence/`
folder. If `commits` flags a subject line, that commit's already in history,
note it and write better subject lines going forward rather than rewriting
published history.

## Step 4 — Re-run to confirm

```bash
python code/repo_audit.py structure --repo-root ../../..
python code/repo_audit.py commits --repo-root ../../..
```
Expected output: fewer (ideally zero) issues than the first run.

## Step 5 — Save evidence

```bash
mkdir -p evidence
python code/repo_audit.py structure --repo-root ../../.. > evidence/structure-audit-after.txt
python code/repo_audit.py commits --repo-root ../../.. > evidence/commits-audit.txt
```
Keep the "before" run from Step 1 alongside the "after" run, the gap between
them is the actual evidence that the tool did something, not just that it
printed PASS.
