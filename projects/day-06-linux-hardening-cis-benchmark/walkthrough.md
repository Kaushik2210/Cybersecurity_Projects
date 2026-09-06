# Day 06 — Walkthrough

Exact commands, in order, with what to expect at each step.

## Step 1 — Run the checker on a fresh VM/container

```bash
chmod +x code/cis_check.sh
./code/cis_check.sh
```
Expected output: a fresh, unhardened Debian/Ubuntu box should fail several
checks, commonly SSH root login, password max age (Debian defaults to
`PASS_MAX_DAYS 99999`), default umask (`022`), and `auditd` not installed.
Exit code is non-zero when anything fails.

## Step 2 — Read the report before doing anything else

Don't run the hardener yet. Look at each FAIL and understand *why* it's a
CIS control, not just that a script said so.

## Step 3 — Run the hardener as root

```bash
sudo chmod +x code/cis_harden.sh
sudo ./code/cis_harden.sh
```
Expected output: a line per fix applied, and a note that every touched file
was backed up first. Confirm the backups exist:
```bash
ls -la /etc/*.bak.* /etc/ssh/*.bak.*
```

## Step 4 — Re-run the checker to confirm

```bash
./code/cis_check.sh
```
Expected output: all 10 checks PASS, exit code 0.

## Step 5 — Run real Lynis for comparison

```bash
sudo apt-get install -y lynis
sudo lynis audit system --quick
```
Expected output: a full audit covering roughly 200+ checks, far more than
the 10 in `cis_check.sh`, ending with a hardening index score (0-100). For
a genuine before/after, run this on a fresh, unhardened copy of the VM
first, then again after Step 3, rather than only running it once.

## Step 6 — Save evidence

```bash
mkdir -p evidence
./code/cis_check.sh > evidence/cis-check-before.txt   # run before Step 3
sudo ./code/cis_harden.sh 2>&1 | tee evidence/cis-harden-output.txt
./code/cis_check.sh > evidence/cis-check-after.txt
sudo cp /var/log/lynis-report.dat evidence/lynis-report-after.dat
```
