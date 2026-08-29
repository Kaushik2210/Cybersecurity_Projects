# Dependencies

`host_recon.sh` is plain bash — no package manager install needed beyond what
ships on a standard Kali/Ubuntu install. It uses (and degrades gracefully if
one is missing):

- `bash` 4+ (default on both distros)
- coreutils: `awk`, `find`, `grep`, `sort`, `date`, `hostname`, `uptime`
- `iproute2` (`ss`) — listening ports
- `systemd` (`systemctl`) — enabled services (skipped with a note on non-systemd systems)
- `util-linux` (`last`, `lastb`) — login history
- `cron`/`cronie` (`crontab`) — scheduled tasks

If a tool is missing, the script prints a note explaining what's missing
instead of crashing — see `run_or_note()` in the script.
