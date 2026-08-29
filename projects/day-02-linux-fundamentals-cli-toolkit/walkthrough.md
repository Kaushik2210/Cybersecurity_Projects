# Day 02 — Walkthrough

Exact commands, in order, with what to expect at each step.

## Step 1 — Get the script onto your VM

If it's a fresh VM without this repo cloned, copy just the script over:
```bash
scp code/host_recon.sh kaushik@192.168.10.10:~/host_recon.sh
```
Expected output: a progress line ending `100%` and no error.

## Step 2 — Make it executable and run as a normal user

```bash
chmod +x host_recon.sh
./host_recon.sh
```
Expected output: a multi-section report starting with `Host recon report —
<hostname> — <UTC timestamp>` and ending `Report complete.`. The listening
ports and failed-login sections will note that they need root for full
detail.

## Step 3 — Run again with root, and compare

```bash
sudo ./host_recon.sh > /tmp/report-root.txt
./host_recon.sh > /tmp/report-user.txt
diff /tmp/report-user.txt /tmp/report-root.txt
```
Expected output: `diff` shows the sections that gained detail under root —
typically the process names next to listening ports, and the failed-login
history.

## Step 4 — Save evidence

```bash
mkdir -p evidence
cp /tmp/report-root.txt evidence/report-root-$(date +%Y%m%d).txt
cp /tmp/report-user.txt evidence/report-user-$(date +%Y%m%d).txt
```
Before committing, skim both files for anything you don't want public
(real hostnames tied to your identity, etc.) and redact if needed —
these are meant to demonstrate the *tool*, not leak your real lab details.

<!-- Screenshot placeholder: ![](evidence/01-report-run.png) -->

## Step 5 — Try the stretch goal (optional)

Run the script on two different days and manually diff the reports to see
what changed — a new listening port, a package that added a cron job, etc.
This is the manual version of the `--diff` mode suggested in the README's
"Upgrade to Stand Out" section.
