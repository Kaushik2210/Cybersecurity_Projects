#!/usr/bin/env bash
#
# host_recon.sh — a safe, read-only "recon of my own box" report.
#
# WHAT THIS DOES
#   Walks through the same categories a security engineer checks first on any
#   Linux host they're newly responsible for: who/what runs it, who can log
#   in, what's listening on the network, what has elevated privilege, and
#   what's been happening in the logs. Prints a single readable report.
#
# WHY THIS MATTERS
#   This is the "know your own terrain" step. You can't spot something
#   abnormal (a rogue listening port, an unexpected SUID binary, a surprise
#   sudoer) if you've never looked at what normal is for this specific box.
#
# SAFETY
#   Every command here is READ-ONLY — it inspects state, it never changes
#   anything. Some sections (listening-process names, failed-login history)
#   need root to show full detail; the script detects that and says so
#   instead of silently failing or, worse, re-running itself with sudo.
#
# USAGE
#   ./host_recon.sh                  # print the report to stdout
#   ./host_recon.sh > report.txt     # save it
#
set -uo pipefail
# Note: NOT using `set -e` here on purpose. Several commands below are
# expected to legitimately fail on some systems (e.g. no crontab set for this
# user) and we want to report that gracefully, not abort the whole script.

section() {
    # Small helper so every section header looks the same.
    echo
    echo "==== $1 ===="
}

run_or_note() {
    # Run a command; if it fails, print why instead of crashing or going
    # silent. $1 = human description, rest = the actual command + args.
    local description="$1"
    shift
    if ! "$@" 2>/dev/null; then
        echo "(could not read $description — see 'Section notes' below)"
    fi
}

IS_ROOT=false
if [[ "$(id -u)" -eq 0 ]]; then
    IS_ROOT=true
fi

echo "Host recon report — $(hostname) — $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
echo "Run as: $(whoami) (root: $IS_ROOT)"

# --- 1. System identity -----------------------------------------------------
section "System identity"
echo "Kernel:       $(uname -srmo)"
if [[ -r /etc/os-release ]]; then
    # os-release is the standard, distro-agnostic way to get a friendly name.
    grep -E '^(NAME|VERSION)=' /etc/os-release
fi
echo "Uptime:       $(uptime -p 2>/dev/null || uptime)"

# --- 2. Users & groups -------------------------------------------------------
section "Users with an interactive shell"
# Filter /etc/passwd down to accounts that can actually log in interactively
# (real shells, not /usr/sbin/nologin or /bin/false) — that's the list an
# attacker or auditor actually cares about.
awk -F: '$7 !~ /(nologin|false)$/ {printf "  %-20s uid=%s shell=%s\n", $1, $3, $7}' /etc/passwd

section "Members of sudo/wheel (can escalate to root)"
getent group sudo 2>/dev/null
getent group wheel 2>/dev/null
if ! getent group sudo >/dev/null 2>&1 && ! getent group wheel >/dev/null 2>&1; then
    echo "(no sudo or wheel group found on this system)"
fi

# --- 3. Listening network services ------------------------------------------
section "Listening TCP/UDP ports"
if command -v ss >/dev/null 2>&1; then
    if $IS_ROOT; then
        ss -tulnp
    else
        echo "(process names require root — showing ports/addresses only)"
        ss -tuln
    fi
else
    echo "(ss not installed — try: sudo apt install iproute2)"
fi

# --- 4. Running services ------------------------------------------------------
section "Enabled systemd services (start automatically at boot)"
if command -v systemctl >/dev/null 2>&1; then
    systemctl list-unit-files --type=service --state=enabled --no-pager 2>/dev/null \
        | head -n 30
else
    echo "(systemctl not found — this system may not use systemd)"
fi

# --- 5. Privileged binaries ---------------------------------------------------
section "SUID/SGID binaries (run with the file owner's privilege, not the caller's)"
# These are worth knowing about because a SUID binary with a bug is a classic
# privilege-escalation path. This is a common, legitimate set on any Linux
# box (e.g. /usr/bin/passwd) — the point is to know your baseline, not that
# every result here is a problem.
find / -xdev \( -perm -4000 -o -perm -2000 \) -type f 2>/dev/null | sort

# --- 6. World-writable files outside expected locations ----------------------
section "World-writable files outside /tmp, /var/tmp, /dev/shm"
find / -xdev -type f -perm -0002 \
    -not -path '/tmp/*' -not -path '/var/tmp/*' -not -path '/dev/shm/*' \
    2>/dev/null | head -n 30

# --- 7. Scheduled tasks --------------------------------------------------------
section "Current user's crontab"
run_or_note "current user's crontab" crontab -l

section "System-wide cron jobs"
if [[ -d /etc/cron.d ]]; then
    ls -la /etc/cron.d 2>/dev/null
fi

# --- 8. Login history -----------------------------------------------------------
section "Recent successful logins"
run_or_note "login history" last -n 10

section "Recent failed logins"
if $IS_ROOT; then
    run_or_note "failed login history" lastb -n 10
else
    echo "(requires root — /var/log/btmp is not world-readable by design)"
fi

# --- Section notes -----------------------------------------------------------
section "Section notes"
echo "- Some sections show less detail without root (process names on ports,"
echo "  failed-login history). Re-run with sudo for the full picture, but"
echo "  note WHAT you had to elevate for — that's itself useful to document."
echo "- A SUID/world-writable binary showing up here is not automatically a"
echo "  finding. The point of this report is a baseline: run it again after"
echo "  changes and diff the two to see what actually moved."

echo
echo "Report complete."
