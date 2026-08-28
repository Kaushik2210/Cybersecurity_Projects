# Cybersecurity Project Series — The Roadmap

A day-by-day path from absolute basics to advanced, ending portfolio-ready. Built around your original 30 projects and expanded with the areas that are actually being hired for in 2026: AI/LLM security, cloud, identity, and detection engineering.

**How the days work:** most projects span more than one calendar day of real effort. Treat each numbered "Day" as a *unit of work* (a session), not necessarily 24 hours. Some big ones (Home SOC, Active Directory, malware analysis) are explicitly split across multiple days. Total: **100 days / units**, grouped into 8 phases.

**Legend for Level:** 🟢 Beginner · 🟡 Intermediate · 🔴 Advanced

**Framework tags** you'll see: ATT&CK (MITRE ATT&CK), ATLAS (MITRE ATLAS, for AI), OWASP, OWASP-LLM, NIST CSF.

---

## Phase 0 — Foundations & Setup (Days 1–8) 🟢

The unglamorous base that everything else stands on. If you skip this, the later days have nowhere to run.

| Day | Project | Level | Core skills | Stack | Proves | Stretch goal |
|-----|---------|-------|-------------|-------|--------|--------------|
| 1 | Home lab with segmented network | 🟢 | Virtualisation, networking, VLANs, firewall rules | Proxmox or VirtualBox, pfSense, Linux + Windows VMs | You can build and reason about a real network | Prove isolation with a traffic capture showing segments can't talk |
| 2 | Linux fundamentals & CLI security toolkit | 🟢 | Shell, permissions, users, services, logs | Kali/Ubuntu, bash | You're fluent where security work happens | Write a bash "recon of my own box" script, fully commented |
| 3 | Networking & protocols crash-project | 🟢 | TCP/IP, DNS, HTTP(S), TLS handshake | Wireshark, curl, dig | You understand what's on the wire | Diagram a full HTTPS request lifecycle from your own capture |
| 4 | Packet capture analysis writeup | 🟢 | Wireshark, protocol analysis, reporting | Wireshark, public pcap samples | You can read traffic, not just run tools | Analyse a real malware pcap and produce an incident timeline |
| 5 | Git, GitHub & documentation discipline | 🟢 | Version control, markdown, technical writing | git, GitHub, mermaid | Your work is legible and public | Set up the repo README, badges, and a clean commit style |
| 6 | Linux hardening against CIS Benchmark | 🟢 | Hardening, auditing, documentation | Linux, CIS Benchmark, Lynis | Turning a standard into configuration | Automate the hardening with Ansible and re-audit for the delta |
| 7 | Vulnerability assessment of your own lab | 🟢 | Scanning, validation, prioritisation | Nessus Essentials or OpenVAS, your lab | You separate real findings from scanner noise | Rank by exploitability + business impact, not CVSS alone |
| 8 | Password policy & cracking assessment (lab only) | 🟡 | Hashcat, policy analysis, reporting | Hashcat, your lab AD, public wordlists | Why policy matters, shown with evidence | Report crack rates by policy tier; never expose real creds |

---

## Phase 1 — Web Application Security (Days 9–18) 🟢→🔴

The single most common entry point, and the skill set behind bug bounty and AppSec roles.

| Day | Project | Level | Core skills | Stack | Proves | Stretch goal |
|-----|---------|-------|-------------|-------|--------|--------------|
| 9 | Set up a vulnerable-app lab | 🟢 | Docker, target setup | DVWA, OWASP Juice Shop, Metasploitable | You have a legal place to practice | Run all three, document how each isolates from your host |
| 10 | OWASP Top 10 — hands-on tour | 🟢 | The core web vuln classes | Burp Suite Community, Juice Shop | You know the canon | One documented exploit + fix per Top 10 category |
| 11–13 | Complete the PortSwigger Web Security Academy | 🟢→🔴 | Every major web vulnerability class | Burp Suite, PortSwigger labs | Genuine web ability, lab by lab | Finish expert-level labs; write up three in depth |
| 14 | SQL injection deep-dive + parametrised fix | 🟡 | SQLi, prepared statements, WAF basics | Burp, a deliberately vulnerable app | Root-cause understanding, not just exploitation | Show the fix in code and prove the payload now fails |
| 15 | XSS & CSRF: exploit, then defend | 🟡 | Injection, CSP, tokens, same-site cookies | Burp, your lab app | You close what you open | Ship a CSP that blocks your own payload; measure it |
| 16 | Web application secure code review | 🔴 | Manual review, SAST, remediation | Semgrep, a real open-source app | Finding what scanners miss | Report findings upstream responsibly; track the fix |
| 17 | Bug bounty findings on a real programme | 🔴 | Recon, web exploitation, disclosure | Burp, Nuclei, HackerOne/Bugcrowd | Real findings on real systems, legally | Get one valid report accepted; write up the methodology |
| 18 | Security architecture review of an application | 🔴 | Threat modelling, STRIDE, control design | Threat model doc, a real app | Design-phase security (the cheapest kind) | Produce a threat model + a prioritised control set |

---

## Phase 2 — Offensive & Practical Hacking (Days 19–28) 🟢→🔴

Enumeration → exploitation → privilege escalation, plus the reporting nobody practices.

| Day | Project | Level | Core skills | Stack | Proves | Stretch goal |
|-----|---------|-------|-------------|-------|--------|--------------|
| 19–21 | Ten TryHackMe rooms with written reports | 🟢 | Enum, exploitation, priv-esc | TryHackMe, Kali | Practical ability + reporting | Write each report as if for a paying client |
| 22 | Build a security tool you wrote yourself | 🟡 | Python, APIs, tool design, docs | Python, target problem of your choice | Engineering ability + security knowledge | Publish it, document it, get one external user |
| 23 | Network scanner & service enumerator (your tool) | 🟡 | Sockets, threading, banner grabbing | Python, your lab | You understand tools by building one | Add safe rate-limiting and a clean report output |
| 24–25 | Active Directory lab & attack-path mapping | 🟡 | AD, Kerberos, BloodHound, lateral movement | Windows Server, BloodHound, Impacket | The environment enterprises actually run | Map the path to domain admin, close it, re-test |
| 26 | CTF competition participation | 🟡 | Broad skills under time pressure | picoCTF, CTFtime events | Verifiable competitive evidence | Publish write-ups for every challenge you solved |
| 27 | Purple team exercise | 🔴 | Attack sim, detection validation, gap analysis | Atomic Red Team or Caldera, your SIEM | Bridging offense and defense | Publish a before/after detection-coverage matrix |
| 28 | Phishing simulation & awareness programme (lab) | 🟡 | Social engineering, metrics, training design | GoPhish, your own lab domain | The human layer, where breaches start | Measure click rate before and after training |

---

## Phase 3 — Blue Team, SOC & Detection (Days 29–42) 🟡→🔴

The most employable defensive skill set, and where a lot of first jobs actually are.

| Day | Project | Level | Core skills | Stack | Proves | Stretch goal |
|-----|---------|-------|-------------|-------|--------|--------------|
| 29–31 | Home SOC with SIEM & detections | 🟡 | Log collection, SIEM, detection rules, alerting | Security Onion or ELK, Sysmon, Wazuh | The core blue-team skill set | Attack your own lab and detect it with rules you wrote |
| 32–33 | Detection engineering with Sigma rules | 🟡 | MITRE ATT&CK, Sigma, false-positive tuning | Sigma, Atomic Red Team, your SIEM | Writing detections, not just consuming | Publish rules; report the false-positive rate honestly |
| 34 | Windows telemetry & Sysmon deep-dive | 🟡 | Endpoint logging, event IDs, config tuning | Sysmon, Windows Event Logs | You know what "good logging" looks like | Tune a Sysmon config and show noise reduction |
| 35–36 | Full incident response simulation | 🟡 | IR lifecycle, containment, evidence, reporting | Your lab, Velociraptor, Autopsy | The judgement interviews probe hardest | Produce a complete incident report + post-mortem |
| 37 | Incident response playbook library | 🟡 | Process design, technical writing, testing | Markdown, your lab, real scenarios | You make teams faster | Have someone follow a playbook cold; fix what confused them |
| 38 | Log analysis & anomaly detection at scale | 🔴 | Python, statistics, log parsing, tuning | Python, real log datasets | Detection beyond signature matching | Compare against a signature baseline with real numbers |
| 39 | Threat intelligence enrichment pipeline | 🟡 | APIs, IOC enrichment, automation, MISP | Python, MISP or OpenCTI, public feeds | Turning raw indicators into intelligence | Automate enrichment and feed it into your SIEM |
| 40 | Open-source contribution to a security tool | 🟡 | Reading unfamiliar code, tests, review | Nuclei templates, Sigma rules, or a tool you use | Working in public, reviewed by practitioners | Get a detection rule/template merged upstream |
| 41 | SOC automation / SOAR-lite | 🟡 | Playbook automation, APIs, orchestration | Python, Shuffle or n8n, your SIEM | You remove toil, not just detect | Auto-triage one alert type end to end, measured |
| 42 | Purple team coverage report (capstone of phase) | 🔴 | ATT&CK coverage mapping, honest reporting | ATT&CK Navigator, your detections | You can show your gaps, not hide them | Publish a Navigator layer of what you can and can't detect |

---

## Phase 4 — Malware Analysis & Digital Forensics (Days 43–52) 🔴

Advanced, careful, isolated. This is where the "Scope & Legal" and isolated-VM discipline matters most.

| Day | Project | Level | Core skills | Stack | Proves | Stretch goal |
|-----|---------|-------|-------------|-------|--------|--------------|
| 43 | Build an isolated analysis lab | 🔴 | Sandboxing, network isolation, snapshots | REMnux, FlareVM, isolated VLAN | You can handle samples safely | Prove the sandbox has no route to your real network |
| 44–45 | Malware analysis of a real sample | 🔴 | Static + dynamic analysis, sandboxing, YARA | REMnux, Ghidra, Any.run, isolated VM | Analysis capability, done safely | Write a YARA rule that detects the family; test it |
| 46 | YARA rule writing & testing | 🔴 | Signatures, string analysis, tuning | YARA, sample corpus | Detection authoring for real | Measure your rule's true/false positive rate |
| 47–48 | Memory forensics investigation | 🔴 | Volatility, process analysis, timeline recon | Volatility, public memory images | Finding what never touched disk | Reconstruct the full attack timeline from memory alone |
| 49 | Disk & file-system forensics | 🔴 | Imaging, artifacts, timelines | Autopsy, public disk images | Evidence handling and chain of custody | Produce a defensible, court-style artifact timeline |
| 50 | Phishing email & attachment analysis | 🟡 | Header analysis, static doc/macro triage | Public samples, oletools, isolated VM | Real SOC daily work | Turn one email into a full IOC + detection package |
| 51 | Reverse engineering a simple binary | 🔴 | Ghidra, assembly basics, control flow | Ghidra, a CTF-style binary | You can read compiled code | Document the algorithm you recovered, step by step |
| 52 | Threat report on a real campaign (OSINT) | 🟡 | Research, attribution caution, writing | Public reporting, MITRE ATT&CK | You synthesise intel like an analyst | Map the campaign to ATT&CK and write an exec summary |

---

## Phase 5 — Cloud, Container & DevSecOps (Days 53–66) 🟡→🔴

The fastest-growing area of security hiring. Uses free tiers so it costs nothing.

| Day | Project | Level | Core skills | Stack | Proves | Stretch goal |
|-----|---------|-------|-------------|-------|--------|--------------|
| 53 | Cloud fundamentals & free-tier setup | 🟡 | IAM basics, billing guardrails | AWS or Azure free tier | You can operate in cloud safely | Set a hard budget alarm; document least-privilege from day 1 |
| 54–55 | Cloud security audit & remediation | 🟡 | IAM, misconfig, logging, CSPM | AWS/Azure free tier, Prowler or ScoutSuite | The fastest-growing hiring area | Add preventative guardrails so the misconfig can't recur |
| 56 | IAM privilege-escalation lab (cloud) | 🔴 | Policy analysis, escalation paths | AWS, IAM policies, pmapper | You understand cloud identity risk | Map an escalation path, then write the SCP that blocks it |
| 57 | Cloud logging & detection (CloudTrail/Sentinel) | 🟡 | Cloud-native logging, detections | CloudTrail + Athena, or Azure Sentinel | Detection in the cloud, not just on-prem | Detect a simulated attack from cloud logs alone |
| 58–59 | DevSecOps pipeline with security gates | 🟡 | SAST, SCA, secrets, IaC scanning | GitHub Actions, Semgrep, Trivy, gitleaks | Security built into delivery | Show the build failing on a real CVE and a leaked secret |
| 60 | Container image scanning & hardening | 🟡 | Image layers, CVEs, minimal images | Docker, Trivy, distroless | You ship safer artifacts | Cut a real image's CVE count and document how |
| 61 | Infrastructure-as-Code security | 🟡 | IaC scanning, policy-as-code | Terraform, tfsec/Checkov, OPA | You catch misconfig before deploy | Write an OPA policy that blocks a bad Terraform plan |
| 62–63 | Kubernetes security assessment | 🔴 | RBAC, network policy, image scanning, runtime | Kubernetes Goat, kube-bench, Falco | Securing the modern deploy layer | Harden the cluster; prove each attack now fails |
| 64 | Secrets management done right | 🟡 | Vaulting, rotation, leak prevention | Vault or cloud KMS, gitleaks | You stop the most common breach cause | Migrate a hard-coded secret to a vault; prove it's gone |
| 65 | Supply-chain security (SBOM + signing) | 🔴 | SBOM, provenance, artifact signing | Syft, Grype, Sigstore/cosign | You address the 2026 supply-chain concern | Generate an SBOM, sign an artifact, verify the signature |
| 66 | Zero trust architecture design | 🔴 | Identity, segmentation, policy, monitoring | Design document, your lab | Architecture thinking, not tool operation | Implement one component; measure its operational cost |

---

## Phase 6 — AI / LLM Security (Days 67–82) 🟡→🔴

The area 2026 job postings are actively asking for: PyRIT, Garak, Promptfoo, OWASP LLM Top 10, MITRE ATLAS, adversarial testing of RAG and agentic/MCP systems. This is your differentiator — few student portfolios have it.

| Day | Project | Level | Core skills | Stack | Proves | Stretch goal |
|-----|---------|-------|-------------|-------|--------|--------------|
| 67 | AI security foundations & threat mapping | 🟡 | OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF | Reading + a diagram | You speak the frameworks recruiters name | Map a sample LLM app to all ten LLM risks + ATLAS techniques |
| 68 | Prompt injection lab (direct) | 🟡 | Injection, jailbreaks, guardrail testing | A local/hosted LLM, your own test app | You can break a model safely | Document 5 payload classes and which guardrails stop them |
| 69 | Indirect / RAG injection lab | 🔴 | RAG poisoning, retrieval trust boundaries | A small RAG app you build, poisoned docs | You test the pipeline, not just the model | Build a poisoned-doc harness; show the leak, then the fix |
| 70–71 | Automated LLM red-teaming with Garak | 🟡 | Scanner-based testing, probe coverage | NVIDIA Garak, a target model | Breadth testing employers ask for by name | Run 120+ probes; triage findings; write an OWASP-mapped report |
| 72–73 | Adversarial testing with PyRIT | 🔴 | Multi-turn orchestration, Crescendo/TAP | Microsoft PyRIT (microsoft/PyRIT) | Depth testing + custom attack chains | Build one custom multi-turn attack and measure success rate |
| 74 | CI security gate with Promptfoo | 🟡 | Eval-driven security, CI integration | Promptfoo, GitHub Actions, OWASP-LLM preset | Security testing as a build gate | Make a PR fail on a new prompt-injection regression |
| 75 | Agentic / MCP security review | 🔴 | Excessive agency, tool abuse, trust boundaries | An agent or MCP setup, OWASP Agentic Top 10 | The newest, hottest sub-area | Threat-model an agent's tools; show one abuse + mitigation |
| 76 | LLM output-handling & data-leak testing | 🟡 | Insecure output handling, PII leakage | Your test app, sample sensitive data | You catch the "LLM09/LLM06" class bugs | Build a red-team suite for data exfil; report leak rate |
| 77 | Build an AI-powered security tool | 🟡 | LLM APIs, prompt design, guardrails | Python, an LLM API | You can build *with* AI, safely | E.g. a log-triage or phishing-triage assistant, with guardrails |
| 78 | ML for security: phishing/URL classifier | 🟡 | Feature engineering, evaluation, honest metrics | Python, scikit-learn, public dataset | Applied ML + security judgement | Report precision/recall honestly; discuss adversarial evasion |
| 79 | Adversarial ML: evade your own classifier | 🔴 | Evasion, robustness, defense | Your Day-78 model | You understand ML's fragility | Craft evasion samples; then harden and re-measure |
| 80 | Anti–password-strength-checker (novel project) | 🟡 | Real-world password risk modelling | Python, breach corpora (HIBP-style, hashed) | You go beyond the clichéd beginner project | Score against real-world crackability, not rule-of-thumb meters |
| 81 | AI incident response & eval regression suite | 🔴 | AI IR, regression evals, gating | Promptfoo/PyRIT, your test app | You close the loop: find → fix → prevent regress | A suite that gates every model/prompt change |
| 82 | Model / RAG security writeup (capstone) | 🔴 | Reporting, framework mapping, communication | Markdown, your findings | You can explain AI risk to humans | Executive summary + technical findings + remediation roadmap |

---

## Phase 7 — GRC, Architecture & Communication (Days 83–92) 🟡→🔴

The judgement-and-communication layer that decides senior hiring. Often the differentiator between "can run tools" and "can be trusted."

| Day | Project | Level | Core skills | Stack | Proves | Stretch goal |
|-----|---------|-------|-------------|-------|--------|--------------|
| 83 | GRC assessment against NIST CSF | 🟡 | Framework mapping, gap analysis, risk reporting | NIST CSF, your lab environment | Translating tech reality into business risk | Produce a board-ready one-page risk summary |
| 84 | Risk assessment & risk register | 🟡 | Likelihood/impact, risk scoring, tracking | Spreadsheet/GRC template | You quantify and prioritise risk | Build a living risk register with owners and due dates |
| 85 | Security policy & standards pack | 🟡 | Policy writing, standards, clarity | Markdown, real templates | You produce the documents orgs need | Write an acceptable-use + IR + access-control policy set |
| 86 | Compliance mapping (ISO 27001 / SOC 2 basics) | 🟡 | Control mapping, evidence thinking | ISO 27001 Annex A / SOC 2 TSC | You understand audits | Map your portfolio's controls to a real framework |
| 87 | Threat modelling a system (STRIDE, deep) | 🔴 | STRIDE, data-flow diagrams, controls | A real app, threat-model tooling | Design-phase security depth | Full DFD + prioritised, mapped control set |
| 88 | Tabletop exercise design & facilitation | 🟡 | Scenario design, facilitation, lessons-learned | Your playbooks, a scenario | You improve teams, not just systems | Run it with a friend; publish the after-action report |
| 89 | Metrics & security dashboard | 🟡 | KPIs, MTTR/MTTD, visualisation | Python/Grafana, your SIEM data | You measure what matters | Build a dashboard tied to real detections from Phase 3 |
| 90 | Public technical writeup or blog | 🟡 | Technical writing, clarity, reproducibility | Markdown, GitHub Pages or Medium | Communication, which decides senior hiring | Publish two writeups; get one shared by a practitioner |
| 91 | Portfolio site & case-study polish | 🟡 | Presentation, curation, storytelling | GitHub Pages / your portfolio | Recruiters find your best work in seconds | Turn your 3 strongest days into recruiter-facing case studies |
| 92 | Resume & narrative alignment | 🟢 | Positioning, role-targeting | Your resume, the NICE framework | Your projects map to a target role | Align every project to one role you actually want |

---

## Phase 8 — Capstones (Days 93–100) 🔴

Bigger, integrative projects that combine several phases. These are the ones you lead with.

| Day | Project | Level | What it integrates | Deliverable |
|-----|---------|-------|--------------------|-------------|
| 93–94 | End-to-end attack & defense narrative | 🔴 | Phases 2 + 3 | Attack your lab, detect it, respond, write the full story with evidence |
| 95–96 | Cloud-native secure app + pipeline | 🔴 | Phases 1 + 5 | A small app, threat-modelled, with a security-gated CI/CD pipeline that visibly blocks bad builds |
| 97 | AI-secured application | 🔴 | Phases 1 + 6 | An LLM feature with a documented red-team + regression eval suite gating changes |
| 98 | Detection-engineering portfolio pack | 🔴 | Phases 3 + 4 | A published set of tuned Sigma/YARA rules with honest false-positive rates and an ATT&CK coverage layer |
| 99 | Full security assessment report (client-style) | 🔴 | Phases 1–7 | Pick one system; deliver a complete pentest-or-audit report: exec summary, findings, remediation roadmap |
| 100 | Series retrospective & roadmap-forward | 🟡 | Everything | A capstone README linking every project, a skills-to-role map, and your next 90 days |

---

## Notes on sequencing and reality

- **You don't have to go strictly in order.** The phases are ordered by dependency (later ones assume the lab and Git discipline from Phase 0), but within/after Phase 3 you can chase whatever role you're targeting first. Targeting SOC? Front-load Phases 3–4. AppSec/bug bounty? Phases 1–2. AI security? You can reach Phase 6 early since it mostly needs Python + an API, not the full lab.
- **The AI-security phase is your edge.** Current listings name PyRIT, Garak, Promptfoo, OWASP LLM Top 10, and MITRE ATLAS explicitly. Few student portfolios show this. Even 4–5 solid days here differentiates you.
- **Evidence beats code.** Every day's `evidence/` folder — your real screenshots, captures, and honest metrics — is what makes the repo read as genuine work rather than generated content.
- **Honesty is a signal.** Reporting real false-positive rates, real crack rates, and "what broke" reads as more senior than a wall of green checkmarks.
- **Safety is non-negotiable.** Everything runs against your own lab, public intentionally-vulnerable targets, or your own accounts. The malware and cloud-IAM days especially: isolate first, document the isolation, then proceed.

## Framework references (put these in your master README)

- OWASP Top 10 (web) and OWASP LLM Top 10 (2025 edition) — the two lingua francas.
- OWASP Agentic Top 10 — for agent/MCP work (Phase 6).
- MITRE ATT&CK — detection and purple-team mapping (Phases 2–4).
- MITRE ATLAS — the AI/ML adversary knowledge base (Phase 6).
- NIST CSF and NIST AI RMF — the risk and governance framing (Phases 6–7).
- NICE Workforce Framework — to map projects to real job roles (Phase 7).
