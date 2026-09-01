# Cybersecurity Project Series — 100 Days, 8 Phases

![Days in progress](https://img.shields.io/badge/days-5%2F100_in_progress-blue)
![Level range](https://img.shields.io/badge/level-beginner%20to%20advanced-informational)
![Scope](https://img.shields.io/badge/scope-authorized%20lab%20%26%20public%20targets%20only-important)
![License](https://img.shields.io/badge/license-educational%20use-lightgrey)

A day-by-day cybersecurity learning portfolio: Linux and network fundamentals →
web app security → offensive fundamentals → blue team/SOC → malware & forensics
→ cloud/container/DevSecOps → **AI/LLM security** → GRC & communication →
capstones. See [`ROADMAP.md`](./ROADMAP.md) for the full plan and
[`PROGRESS.md`](./PROGRESS.md) for the day-by-day checklist.

**Author:** Kaushik · MCA student
**Status:** 🟢 In progress — see the table below

Documentation and commit-message discipline for this repo are checked with
[`projects/day-05-git-github-documentation-discipline/code/repo_audit.py`](./projects/day-05-git-github-documentation-discipline/code/repo_audit.py)
rather than just asserted.

---

## Scope & Legal

Every project in this repo runs against a personal home lab, a public
intentionally-vulnerable target (DVWA, OWASP Juice Shop, Metasploitable,
HackTheBox, TryHackMe, PortSwigger Web Security Academy, picoCTF), or the
author's own accounts. **Nothing here is run against third-party systems
without authorization.** Where a topic touches offensive tooling (malware
analysis, password cracking, phishing simulation), the project builds the
analysis/detection/measurement side using inert public samples in isolated
environments — never functional malware or real payloads. Every project's
README repeats this in a "Scope & Legal" section.

## How this repo is organized

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the folder layout and the
standard every project follows.

## Frameworks referenced throughout

OWASP Top 10 · OWASP LLM Top 10 · OWASP Agentic Top 10 · MITRE ATT&CK ·
MITRE ATLAS · NIST CSF · NIST AI RMF · NICE Workforce Framework

---

## Progress

| Day | Project | Level | Phase | Status |
|-----|---------|-------|-------|--------|
| 01 | [Home lab with segmented network](./projects/day-01-home-lab-segmented-network/README.md) | 🟢 | 0 — Foundations | 🟨 |
| 02 | [Linux fundamentals & CLI security toolkit](./projects/day-02-linux-fundamentals-cli-toolkit/README.md) | 🟢 | 0 — Foundations | 🟨 |
| 03 | [Networking & protocols crash-project](./projects/day-03-networking-protocols-crash-project/README.md) | 🟢 | 0 — Foundations | 🟨 |
| 04 | [Packet capture analysis writeup](./projects/day-04-packet-capture-analysis/README.md) | 🟢 | 0 — Foundations | 🟨 |
| 05 | [Git, GitHub & documentation discipline](./projects/day-05-git-github-documentation-discipline/README.md) | 🟢 | 0 — Foundations | ✅ |
| 06 | Linux hardening against CIS Benchmark | 🟢 | 0 — Foundations | ⬜ |
| 07 | Vulnerability assessment of your own lab | 🟢 | 0 — Foundations | ⬜ |
| 08 | Password policy & cracking assessment (lab only) | 🟡 | 0 — Foundations | ⬜ |
| 09 | Set up a vulnerable-app lab | 🟢 | 1 — Web AppSec | ⬜ |
| 10 | OWASP Top 10 — hands-on tour | 🟢 | 1 — Web AppSec | ⬜ |
| 11–13 | PortSwigger Web Security Academy | 🟢→🔴 | 1 — Web AppSec | ⬜ |
| 14 | SQL injection deep-dive + parametrised fix | 🟡 | 1 — Web AppSec | ⬜ |
| 15 | XSS & CSRF: exploit, then defend | 🟡 | 1 — Web AppSec | ⬜ |
| 16 | Web application secure code review | 🔴 | 1 — Web AppSec | ⬜ |
| 17 | Bug bounty findings on a real programme | 🔴 | 1 — Web AppSec | ⬜ |
| 18 | Security architecture review of an application | 🔴 | 1 — Web AppSec | ⬜ |
| 19–21 | Ten TryHackMe rooms with written reports | 🟢 | 2 — Offensive | ⬜ |
| 22 | Build a security tool you wrote yourself | 🟡 | 2 — Offensive | ⬜ |
| 23 | Network scanner & service enumerator | 🟡 | 2 — Offensive | ⬜ |
| 24–25 | Active Directory lab & attack-path mapping | 🟡 | 2 — Offensive | ⬜ |
| 26 | CTF competition participation | 🟡 | 2 — Offensive | ⬜ |
| 27 | Purple team exercise | 🔴 | 2 — Offensive | ⬜ |
| 28 | Phishing simulation & awareness programme (lab) | 🟡 | 2 — Offensive | ⬜ |
| 29–31 | Home SOC with SIEM & detections | 🟡 | 3 — Blue Team | ⬜ |
| 32–33 | Detection engineering with Sigma rules | 🟡 | 3 — Blue Team | ⬜ |
| 34 | Windows telemetry & Sysmon deep-dive | 🟡 | 3 — Blue Team | ⬜ |
| 35–36 | Full incident response simulation | 🟡 | 3 — Blue Team | ⬜ |
| 37 | Incident response playbook library | 🟡 | 3 — Blue Team | ⬜ |
| 38 | Log analysis & anomaly detection at scale | 🔴 | 3 — Blue Team | ⬜ |
| 39 | Threat intelligence enrichment pipeline | 🟡 | 3 — Blue Team | ⬜ |
| 40 | Open-source contribution to a security tool | 🟡 | 3 — Blue Team | ⬜ |
| 41 | SOC automation / SOAR-lite | 🟡 | 3 — Blue Team | ⬜ |
| 42 | Purple team coverage report | 🔴 | 3 — Blue Team | ⬜ |
| 43 | Build an isolated analysis lab | 🔴 | 4 — Malware/Forensics | ⬜ |
| 44–45 | Malware analysis of a real sample | 🔴 | 4 — Malware/Forensics | ⬜ |
| 46 | YARA rule writing & testing | 🔴 | 4 — Malware/Forensics | ⬜ |
| 47–48 | Memory forensics investigation | 🔴 | 4 — Malware/Forensics | ⬜ |
| 49 | Disk & file-system forensics | 🔴 | 4 — Malware/Forensics | ⬜ |
| 50 | Phishing email & attachment analysis | 🟡 | 4 — Malware/Forensics | ⬜ |
| 51 | Reverse engineering a simple binary | 🔴 | 4 — Malware/Forensics | ⬜ |
| 52 | Threat report on a real campaign (OSINT) | 🟡 | 4 — Malware/Forensics | ⬜ |
| 53 | Cloud fundamentals & free-tier setup | 🟡 | 5 — Cloud/DevSecOps | ⬜ |
| 54–55 | Cloud security audit & remediation | 🟡 | 5 — Cloud/DevSecOps | ⬜ |
| 56 | IAM privilege-escalation lab (cloud) | 🔴 | 5 — Cloud/DevSecOps | ⬜ |
| 57 | Cloud logging & detection | 🟡 | 5 — Cloud/DevSecOps | ⬜ |
| 58–59 | DevSecOps pipeline with security gates | 🟡 | 5 — Cloud/DevSecOps | ⬜ |
| 60 | Container image scanning & hardening | 🟡 | 5 — Cloud/DevSecOps | ⬜ |
| 61 | Infrastructure-as-Code security | 🟡 | 5 — Cloud/DevSecOps | ⬜ |
| 62–63 | Kubernetes security assessment | 🔴 | 5 — Cloud/DevSecOps | ⬜ |
| 64 | Secrets management done right | 🟡 | 5 — Cloud/DevSecOps | ⬜ |
| 65 | Supply-chain security (SBOM + signing) | 🔴 | 5 — Cloud/DevSecOps | ⬜ |
| 66 | Zero trust architecture design | 🔴 | 5 — Cloud/DevSecOps | ⬜ |
| 67 | AI security foundations & threat mapping | 🟡 | 6 — AI/LLM Security | ⬜ |
| 68 | Prompt injection lab (direct) | 🟡 | 6 — AI/LLM Security | ⬜ |
| 69 | Indirect / RAG injection lab | 🔴 | 6 — AI/LLM Security | ⬜ |
| 70–71 | Automated LLM red-teaming with Garak | 🟡 | 6 — AI/LLM Security | ⬜ |
| 72–73 | Adversarial testing with PyRIT | 🔴 | 6 — AI/LLM Security | ⬜ |
| 74 | CI security gate with Promptfoo | 🟡 | 6 — AI/LLM Security | ⬜ |
| 75 | Agentic / MCP security review | 🔴 | 6 — AI/LLM Security | ⬜ |
| 76 | LLM output-handling & data-leak testing | 🟡 | 6 — AI/LLM Security | ⬜ |
| 77 | Build an AI-powered security tool | 🟡 | 6 — AI/LLM Security | ⬜ |
| 78 | ML for security: phishing/URL classifier | 🟡 | 6 — AI/LLM Security | ⬜ |
| 79 | Adversarial ML: evade your own classifier | 🔴 | 6 — AI/LLM Security | ⬜ |
| 80 | Anti–password-strength-checker | 🟡 | 6 — AI/LLM Security | ⬜ |
| 81 | AI incident response & eval regression suite | 🔴 | 6 — AI/LLM Security | ⬜ |
| 82 | Model / RAG security writeup (capstone) | 🔴 | 6 — AI/LLM Security | ⬜ |
| 83 | GRC assessment against NIST CSF | 🟡 | 7 — GRC & Comms | ⬜ |
| 84 | Risk assessment & risk register | 🟡 | 7 — GRC & Comms | ⬜ |
| 85 | Security policy & standards pack | 🟡 | 7 — GRC & Comms | ⬜ |
| 86 | Compliance mapping (ISO 27001 / SOC 2 basics) | 🟡 | 7 — GRC & Comms | ⬜ |
| 87 | Threat modelling a system (STRIDE, deep) | 🔴 | 7 — GRC & Comms | ⬜ |
| 88 | Tabletop exercise design & facilitation | 🟡 | 7 — GRC & Comms | ⬜ |
| 89 | Metrics & security dashboard | 🟡 | 7 — GRC & Comms | ⬜ |
| 90 | Public technical writeup or blog | 🟡 | 7 — GRC & Comms | ⬜ |
| 91 | Portfolio site & case-study polish | 🟡 | 7 — GRC & Comms | ⬜ |
| 92 | Resume & narrative alignment | 🟢 | 7 — GRC & Comms | ⬜ |
| 93–94 | End-to-end attack & defense narrative | 🔴 | 8 — Capstones | ⬜ |
| 95–96 | Cloud-native secure app + pipeline | 🔴 | 8 — Capstones | ⬜ |
| 97 | AI-secured application | 🔴 | 8 — Capstones | ⬜ |
| 98 | Detection-engineering portfolio pack | 🔴 | 8 — Capstones | ⬜ |
| 99 | Full security assessment report (client-style) | 🔴 | 8 — Capstones | ⬜ |
| 100 | Series retrospective & roadmap-forward | 🟡 | 8 — Capstones | ⬜ |

*Status column: ⬜ not started · 🟨 in progress · ✅ done — kept in sync with [`PROGRESS.md`](./PROGRESS.md).*
