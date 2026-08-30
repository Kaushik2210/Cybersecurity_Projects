# Evidence — Day 02

## What's actually in here

Real output from a real Linux box: a `debian:12-slim` Docker container, not
the Kali/Ubuntu VM described in the README (that VM build is still pending).
The container had a non-root user (`kaushik`, in the `sudo` group), a real
`/etc/cron.d` job, and standard Debian packages installed, then
`host_recon.sh` was copied in and run twice: once as `kaushik`, once as
`root`.

- `report-user.txt` — run as the non-root user. Note the SUID binary list is
  real (`/usr/bin/passwd`, `/usr/bin/sudo`, etc., straight from this Debian
  image), the listening-ports and failed-login sections correctly report
  they need root, and the cron job I added (`log-cleanup`) shows up under
  system-wide cron jobs.
- `report-root.txt` — the same script, same container, run as root.
- `report-diff.txt` — a plain `diff` of the two, showing exactly what
  changed with elevation: the "root: false/true" line, the listening-port
  detail note disappearing, and `lastb`'s failed-login output actually
  appearing.
- `docker-container-info.txt` — `docker ps` output confirming the container
  this ran in.

## What this doesn't cover yet

This is a single fresh container, not a Kali/Ubuntu VM with real usage
history, so "recent successful logins" is nearly empty and there's no
interesting failed-login history to show. The real VM lab will have more to
report there. `systemctl` also isn't present, since containers don't run
systemd by default — the script's fallback message for that is itself
genuine output, not a stub.

## Still to add

Once the Kali/Ubuntu VM from the main lab is running: a fresh pair of
reports from that VM, and ideally some deliberate "noise" (an extra sudoer,
a cron job, an unexpected SUID binary) to show the report actually catching
something.
