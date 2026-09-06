#!/usr/bin/env bash
#
# cis_harden.sh — apply fixes for the checks in cis_check.sh that failed.
#
# WHY THIS IS A SEPARATE SCRIPT FROM cis_check.sh
#   Checking a system and changing it should never be the same command —
#   that's the difference between an audit and an incident. Run cis_check.sh
#   first, read what it says, THEN decide whether to run this.
#
# WHAT THIS CHANGES
#   - /etc/passwd, /etc/shadow permissions and shadow ownership
#   - /etc/ssh/sshd_config: PermitRootLogin no, PermitEmptyPasswords no
#   - /etc/login.defs: PASS_MAX_DAYS 365, UMASK 027
#   - /proc/sys/fs/suid_dumpable and net.ipv4.ip_forward (best-effort — these
#     are runtime sysctl values, not persisted here; a real deployment would
#     also set them in /etc/sysctl.d/ so they survive a reboot)
#   - installs auditd if a package manager is available
#
# SAFETY
#   Every file this touches gets a timestamped .bak copy next to it first.
#   This is written for a lab VM or throwaway container, NOT for running
#   against a production system without reading every line first — some of
#   these changes (SSH config in particular) can lock you out of a real
#   remote box if done carelessly (e.g. disabling root login before
#   confirming a non-root sudo user actually works).
#
# USAGE
#   sudo ./cis_harden.sh
#
set -uo pipefail

if [[ "$(id -u)" -ne 0 ]]; then
    echo "This needs root to edit /etc/shadow and sshd_config. Re-run with sudo."
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d%H%M%S)

backup_and_edit() {
    # $1 = file to back up before editing
    local file="$1"
    if [[ -f "$file" ]]; then
        cp -p "$file" "${file}.bak.${TIMESTAMP}"
    fi
}

echo "Applying CIS hardening fixes — backups saved with .bak.${TIMESTAMP} suffix"
echo "---------------------------------------------------------------------------"

# --- /etc/passwd and /etc/shadow permissions --------------------------------
backup_and_edit /etc/passwd
chmod 644 /etc/passwd
echo "chmod 644 /etc/passwd"

if [[ -f /etc/shadow ]]; then
    backup_and_edit /etc/shadow
    chmod 640 /etc/shadow
    chown root:shadow /etc/shadow 2>/dev/null || chown root:root /etc/shadow
    echo "chmod 640 /etc/shadow, owner set to root:shadow (or root:root if shadow group absent)"
fi

# --- sshd_config -------------------------------------------------------------
sshd_config="/etc/ssh/sshd_config"
if [[ -f "$sshd_config" ]]; then
    backup_and_edit "$sshd_config"

    if grep -qiE '^\s*#?\s*PermitRootLogin\b' "$sshd_config"; then
        sed -i -E 's/^\s*#?\s*PermitRootLogin\b.*/PermitRootLogin no/' "$sshd_config"
    else
        echo "PermitRootLogin no" >> "$sshd_config"
    fi
    echo "sshd_config: PermitRootLogin no"

    if grep -qiE '^\s*#?\s*PermitEmptyPasswords\b' "$sshd_config"; then
        sed -i -E 's/^\s*#?\s*PermitEmptyPasswords\b.*/PermitEmptyPasswords no/' "$sshd_config"
    else
        echo "PermitEmptyPasswords no" >> "$sshd_config"
    fi
    echo "sshd_config: PermitEmptyPasswords no"
else
    echo "sshd not installed — skipping SSH hardening"
fi

# --- login.defs ----------------------------------------------------------------
login_defs="/etc/login.defs"
if [[ -f "$login_defs" ]]; then
    backup_and_edit "$login_defs"

    if grep -qE '^PASS_MAX_DAYS' "$login_defs"; then
        sed -i -E 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   365/' "$login_defs"
    else
        echo "PASS_MAX_DAYS   365" >> "$login_defs"
    fi
    echo "login.defs: PASS_MAX_DAYS 365"

    if grep -qE '^UMASK' "$login_defs"; then
        sed -i -E 's/^UMASK.*/UMASK           027/' "$login_defs"
    else
        echo "UMASK           027" >> "$login_defs"
    fi
    echo "login.defs: UMASK 027"
fi

# --- Runtime sysctl values (best-effort — not persisted across reboot here) ---
if [[ -w /proc/sys/fs/suid_dumpable ]]; then
    echo 0 > /proc/sys/fs/suid_dumpable 2>/dev/null \
        && echo "fs.suid_dumpable set to 0 (runtime only — add to /etc/sysctl.d/ to persist)" \
        || echo "could not set fs.suid_dumpable (likely blocked by container runtime)"
fi

if [[ -w /proc/sys/net/ipv4/ip_forward ]]; then
    echo 0 > /proc/sys/net/ipv4/ip_forward 2>/dev/null \
        && echo "net.ipv4.ip_forward set to 0 (runtime only — add to /etc/sysctl.d/ to persist)" \
        || echo "could not set net.ipv4.ip_forward (likely blocked by container runtime)"
fi

# --- auditd --------------------------------------------------------------------
if ! command -v auditctl >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
        apt-get update -qq && apt-get install -y -qq auditd >/dev/null 2>&1 \
            && echo "auditd installed" \
            || echo "auditd install failed — install manually"
    else
        echo "no apt-get available — install auditd manually"
    fi
else
    echo "auditd already installed"
fi

echo "---------------------------------------------------------------------------"
echo "Done. Run cis_check.sh again to confirm the fixes took."
