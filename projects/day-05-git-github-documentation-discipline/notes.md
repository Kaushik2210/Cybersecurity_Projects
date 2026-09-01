# Day 05 — Notes

## What I learned

Building the commit checker was a good reminder that `git log`'s pretty
format placeholders don't always mean what their names suggest. `%b` sounds
like "everything after the subject," including whatever separates them, but
git has already normalized that away by the time it hands the string back.
Anyone writing tooling around `git log` output should check the actual
string, not just the docs, before trusting a placeholder does what its name
implies.

Also worth noting: the very first real run of the structure audit caught a
real, true gap, Day 05's own docs didn't exist yet when I ran it. That's
exactly the kind of self-referential proof that a "does the thing actually
work" test should produce, not a synthetic example built to look good.

## What broke and how I fixed it

- The blank-line-between-subject-and-body check flagged all 8 commits on the
  first run, a 100% false-positive rate, which is itself a strong signal
  something was wrong with the check, not the commits. Root cause: using
  `%s`/`%b` instead of the raw `%B` message. Fixed by switching to `%B` and
  parsing the blank line manually.
- Running the structure audit against a nonexistent repo root threw a raw
  Python traceback (`FileNotFoundError`) instead of a clean message. Added
  an explicit check for the `projects/` folder before trying to list it.

## Interview questions someone could ask me about this
1. Q: Why does commit subject length matter at all?
   A: Most git UIs and `git log --oneline` truncate long subject lines, so
   anything past roughly 72 characters effectively loses its ending for
   anyone skimming history.

2. Q: What went wrong with the first version of the commit checker?
   A: `%b` looked like the right field for "commit body" but git strips the
   separating blank line before returning it, so the check fired on every
   commit, including correctly-formatted ones. Fixed by using the raw `%B`
   message and checking the blank line by hand.

3. Q: Why check documentation structure with a script instead of reviewing by hand?
   A: Manual review doesn't scale and is inconsistent between reviews. A
   mechanical check is boring but exhaustive, and it's the same shape as the
   config-compliance tools used later in the series.

4. Q: How would you make this actually enforce the standard instead of just reporting on it?
   A: Wire it into a CI step that fails the build on a nonzero exit code,
   same pattern as the Day 58-59 security-gated pipeline.
