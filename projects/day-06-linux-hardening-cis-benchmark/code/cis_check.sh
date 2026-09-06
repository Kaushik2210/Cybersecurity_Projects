#!/usr/bin/env bash
#
# cis_check.sh — a small, hand-picked subset of CIS Debian/Ubuntu Benchmark
# controls, checked directly instead of taken on faith from a scanner.
#
# WHY BUILD THIS INSTEAD OF JUST RUNNING LYNIS
#   Lynis (run separately — see walkthrough.md) is the real, industry-used
#   tool for this and reports far more than these ten checks. Building a
#   handful by hand first is what actually teaches what a CIS control means
#   at the file/config level, e.g. "ensure permissions on /etc/shadow are
#   configured" isn't a magic phrase, it's `stat` showing 0640 root:shadow.
#   Lynis' own output gets compared against this in evidence/ afterward.
#
# WHAT IT CHECKS (each maps to a real CIS Debian/Ubuntu Benchmark control)
#   1. /etc/passwd permissions            (world-readable is fine, writable is not)
#   2. /etc/shadow permissions and owner  (root:shadow, not world-readable)
#   3. No accounts with an empty password field in /etc/shadow
#   4. SSH root login disabled            (PermitRootLogin no)
#   5. SSH empty passwords disabled       (PermitEmptyPasswords no)
#   6. Password max age <= 365 days       (PASS_MAX_DAYS in /etc/login.defs)
#   7. Default user umask 027 or stricter (in /etc/login.defs)
#   8. Core dumps restricted              (fs.suid_dumpable = 0)
#   9. IP forwarding disabled             (net.ipv4.ip_forward = 0)
#  10. auditd installed                   (audit trail capability present)
#
# SAFETY
#   Entirely read-only. This never edits a config file — cis_harden.sh (the
#   companion script) does that, deliberately kept separate so "checking"
#   and "changing" a system are never the same command.
#
# USAGE
#   ./cis_check.sh
#
set -uo pipefail

PASS=0
FAIL=0
NA=0

report() {
    # $1 = check id, $2 = description, $3 = PASS|FAIL|N/A, $4 = detail
    local id="$1" desc="$2" result="$3" detail="$4"
    printf "[%-4s] %-45s %-4s  %s\n" "$id" "$desc" "$result" "$detail"
    case "$result" in
        PASS) PASS=$((PASS + 1)) ;;
        FAIL) FAIL=$((FAIL + 1)) ;;
        *)    NA=$((NA + 1)) ;;
    esac
}

echo "CIS Debian/Ubuntu Benchmark — subset check — $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
echo "-----------------------------------------------------------------------------"

# --- 1. /etc/passwd permissions ---------------------------------------------
if [[ -f /etc/passwd ]]; then
    perms=$(stat -c '%a' /etc/passwd)
    if [[ "$perms" -le 644 ]]; then
        report "1.1" "/etc/passwd permissions (<=644)" PASS "mode $perms"
    else
        report "1.1" "/etc/passwd permissions (<=644)" FAIL "mode $perms"
    fi
else
    report "1.1" "/etc/passwd permissions (<=644)" "N/A" "file not found"
fi

# --- 2. /etc/shadow permissions and owner -----------------------------------
if [[ -f /etc/shadow ]]; then
    perms=$(stat -c '%a' /etc/shadow)
    owner=$(stat -c '%U:%G' /etc/shadow)
    if [[ "$perms" -le 640 && ( "$owner" == "root:shadow" || "$owner" == "root:root" ) ]]; then
        report "1.2" "/etc/shadow perms/owner (<=640, root:shadow)" PASS "$perms $owner"
    else
        report "1.2" "/etc/shadow perms/owner (<=640, root:shadow)" FAIL "$perms $owner"
    fi
else
    report "1.2" "/etc/shadow perms/owner (<=640, root:shadow)" "N/A" "file not found"
fi

# --- 3. No empty-password accounts ------------------------------------------
if [[ -r /etc/shadow ]]; then
    empty_pw_accounts=$(awk -F: '($2 == "") {print $1}' /etc/shadow)
    if [[ -z "$empty_pw_accounts" ]]; then
        report "1.3" "No accounts with empty password" PASS "none found"
    else
        report "1.3" "No accounts with empty password" FAIL "$empty_pw_accounts"
    fi
else
    report "1.3" "No accounts with empty password" "N/A" "requires root to read /etc/shadow"
fi

# --- 4 & 5. sshd_config checks -----------------------------------------------
sshd_config="/etc/ssh/sshd_config"
if [[ -f "$sshd_config" ]]; then
    if grep -qiE '^\s*PermitRootLogin\s+no\b' "$sshd_config"; then
        report "5.1" "SSH root login disabled" PASS "PermitRootLogin no"
    else
        report "5.1" "SSH root login disabled" FAIL "not explicitly set to 'no'"
    fi

    if grep -qiE '^\s*PermitEmptyPasswords\s+no\b' "$sshd_config"; then
        report "5.2" "SSH empty passwords disabled" PASS "PermitEmptyPasswords no"
    else
        report "5.2" "SSH empty passwords disabled" FAIL "not explicitly set to 'no'"
    fi
else
    report "5.1" "SSH root login disabled" "N/A" "sshd not installed"
    report "5.2" "SSH empty passwords disabled" "N/A" "sshd not installed"
fi

# --- 6. Password max age -----------------------------------------------------
login_defs="/etc/login.defs"
if [[ -f "$login_defs" ]]; then
    max_days=$(awk '/^PASS_MAX_DAYS/ {print $2}' "$login_defs")
    if [[ -n "$max_days" && "$max_days" -le 365 ]]; then
        report "1.4" "Password max age <= 365 days" PASS "PASS_MAX_DAYS $max_days"
    else
        report "1.4" "Password max age <= 365 days" FAIL "PASS_MAX_DAYS ${max_days:-unset}"
    fi

    # --- 7. Default umask ----------------------------------------------------
    umask_val=$(awk '/^UMASK/ {print $2}' "$login_defs")
    if [[ "$umask_val" == "027" || "$umask_val" == "077" ]]; then
        report "1.5" "Default umask 027 or stricter" PASS "UMASK $umask_val"
    else
        report "1.5" "Default umask 027 or stricter" FAIL "UMASK ${umask_val:-unset}"
    fi
else
    report "1.4" "Password max age <= 365 days" "N/A" "/etc/login.defs not found"
    report "1.5" "Default umask 027 or stricter" "N/A" "/etc/login.defs not found"
fi

# --- 8. Core dumps restricted -------------------------------------------------
if [[ -r /proc/sys/fs/suid_dumpable ]]; then
    dumpable=$(cat /proc/sys/fs/suid_dumpable)
    if [[ "$dumpable" == "0" ]]; then
        report "1.6" "Core dumps restricted (fs.suid_dumpable=0)" PASS "value $dumpable"
    else
        report "1.6" "Core dumps restricted (fs.suid_dumpable=0)" FAIL "value $dumpable"
    fi
else
    report "1.6" "Core dumps restricted (fs.suid_dumpable=0)" "N/A" "/proc/sys not available"
fi

# --- 9. IP forwarding disabled -------------------------------------------------
if [[ -r /proc/sys/net/ipv4/ip_forward ]]; then
    forwarding=$(cat /proc/sys/net/ipv4/ip_forward)
    if [[ "$forwarding" == "0" ]]; then
        report "3.1" "IP forwarding disabled" PASS "value $forwarding"
    else
        report "3.1" "IP forwarding disabled" FAIL "value $forwarding"
    fi
else
    report "3.1" "IP forwarding disabled" "N/A" "/proc/sys not available (container network namespace)"
fi

# --- 10. auditd installed ------------------------------------------------------
if command -v auditctl >/dev/null 2>&1 || dpkg -s auditd >/dev/null 2>&1; then
    report "4.1" "auditd installed" PASS "found"
else
    report "4.1" "auditd installed" FAIL "not installed"
fi

echo "-----------------------------------------------------------------------------"
echo "$PASS passed, $FAIL failed, $NA not applicable."

[[ "$FAIL" -eq 0 ]]
exit $?
