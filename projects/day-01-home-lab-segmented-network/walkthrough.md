# Day 01 — Walkthrough

Exact commands, in order, with what to expect at each step.

## Step 1 — Create isolated internal networks

In VirtualBox: **File → Host Network Manager** is for host-only networks;
for fully isolated segments use **internal networks** instead, set per-VM
under **Settings → Network → Attached to: Internal Network**, and type a
network name (e.g. `intnet-users`). Any two VMs with the same internal
network name can talk to each other and nothing else.

Repeat for `intnet-servers` and `intnet-dmz`.

<!-- Screenshot placeholder: ![](evidence/01-network-manager.png) -->

## Step 2 — Build the router/firewall VM

Create a small Linux VM with **three** network adapters, one per segment
(`intnet-users`, `intnet-servers`, `intnet-dmz`), plus optionally a NAT
adapter if it needs outbound internet for updates.

Enable IP forwarding:
```bash
sudo sysctl -w net.ipv4.ip_forward=1
```
Expected output:
```
net.ipv4.ip_forward = 1
```

Add a default-deny policy between segments, then explicitly allow only the
one path this lab intends (users → dmz on 443):
```bash
sudo nft add table inet filter
sudo nft add chain inet filter forward '{ type filter hook forward priority 0; policy drop; }'
sudo nft add rule inet filter forward iifname "eth0" oifname "eth2" tcp dport 443 accept
```
(Adjust interface names to match your VM's actual NICs — check with `ip a`.)

## Step 3 — Deploy segment VMs

Create one lightweight Linux VM per segment (Alpine/Debian), attach it only
to that segment's internal network, and give it a static IP:
```bash
# on the users-segment VM
sudo ip addr add 192.168.10.10/24 dev eth0
```
Expected output: no output on success; verify with `ip a`.

Repeat for the servers (`192.168.20.10`) and dmz (`192.168.30.10`) VMs.

## Step 4 — Install and configure the checker

On each segment VM:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r code/requirements.txt
cp code/segments.example.yaml code/segments.local.yaml
# edit segments.local.yaml with your real IPs from Step 3
```
Expected output: `pip install` completes with no errors; the file
`code/segments.local.yaml` exists and is gitignored (real IPs shouldn't be
committed).

## Step 5 — Run the check from each segment

On the `users` VM:
```bash
python code/segmentation_check.py code/segments.local.yaml --from-segment users
```
Expected output: a PASS/FAIL table — `dmz` on port 443 should PASS as
reachable, `servers` should PASS as blocked. Any FAIL means either the
firewall rule or the YAML config doesn't match reality — fix and re-run.

Repeat from the `servers` and `dmz` VMs with `--from-segment servers` /
`--from-segment dmz`.

<!-- Screenshot placeholder: ![](evidence/02-checker-output.png) -->

## Step 6 — Capture evidence

On the router VM, capture traffic during a run from a blocked segment to
prove the packets never arrive at the far side:
```bash
sudo tcpdump -i eth1 -w evidence/blocked-attempt.pcap host 192.168.20.10
```
Run the checker from `users` in another terminal, then `Ctrl+C` the capture.
Save the resulting `.pcap` into `evidence/` (sanitize if it contains anything
beyond lab-internal traffic before committing).
