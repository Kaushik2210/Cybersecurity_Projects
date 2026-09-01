# Repo Structure & Conventions

This repo is a personal 100-day cybersecurity learning portfolio, not a
collaborative open-source project — but it's public, so this file explains how
it's organized for anyone visiting.

## Layout

```
cyber-100/
  README.md                     master index: table of all projects, progress tracker
  ROADMAP.md                    the full 100-day / 100-unit plan
  PROGRESS.md                   checklist ticked off day by day
  CONTRIBUTING.md               this file
  .gitignore
  templates/
    PROJECT_README_TEMPLATE.md  the standard every project README follows
    WRITEUP_TEMPLATE.md         incident/analysis writeup skeleton
  scripts/
    new_day.sh                  scaffolds a new day's folder from the template
  projects/
    day-01-<slug>/
    day-02-<slug>/
    ...
```

## Per-project standard

Every `projects/day-NN-<slug>/` folder contains:

- **`README.md`** — follows `templates/PROJECT_README_TEMPLATE.md` exactly. The
  teaching document for that day's topic.
- **`code/`** — the implementation, heavily commented for a beginner, with a
  `requirements.txt` or equivalent.
- **`walkthrough.md`** — a narrated, step-by-step "do this with me" guide with
  exact commands and expected output.
- **`evidence/`** — screenshots, sanitized pcaps, logs, sample outputs. Large or
  sensitive files are gitignored; only sanitized samples are committed.
- **`notes.md`** — what was learned, what broke and how it was fixed, and
  interview Q&A about the project.

## Scaffolding a new day

```bash
./scripts/new_day.sh 07 vulnerability-assessment
```

This creates `projects/day-07-vulnerability-assessment/` pre-populated from
`templates/PROJECT_README_TEMPLATE.md` and the standard sub-folders.

## Checking the standard is actually followed

`projects/day-05-git-github-documentation-discipline/code/repo_audit.py`
checks this repo against the per-project standard above and against a
commit-message style rule, mechanically, instead of trusting a re-read:

```bash
python projects/day-05-git-github-documentation-discipline/code/repo_audit.py structure --repo-root .
python projects/day-05-git-github-documentation-discipline/code/repo_audit.py commits --repo-root .
```

## Safety & ethics

Every project runs against a personal lab, a public intentionally-vulnerable
target (DVWA, Juice Shop, Metasploitable, HackTheBox, TryHackMe, PortSwigger,
picoCTF), or the author's own accounts — never third-party systems without
authorization. Offensive-flavoured topics (malware, cracking, phishing) are
built as analysis/detection/measurement work using inert public samples in
isolated environments. See each project's "Scope & Legal" section.
