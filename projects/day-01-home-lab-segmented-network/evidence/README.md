# Evidence — Day 01

## What's actually in here

The full lab in the main README (VirtualBox internal networks + pfSense/Linux
router VM + one VM per segment) isn't built yet — that's real virtualization
work still on the to-do list. What's in this folder instead is a functional
demo of the same script and the same idea, built with Docker bridge networks
so the reachability checks are real, not staged.

Setup: three containers, three networks.
- `users-host` — attached only to `users-net`
- `dmz-host` — attached to both `users-net` and `dmz-net`, running a real
  HTTP server on port 80
- `servers-host` — attached only to `servers-net`, no shared network with
  `users-host` at all

`docker-demo-segmentation-check.txt` is the real output of running
`segmentation_check.py` against `code/segments.docker-demo.yaml` from inside
`users-host`. Both checks passed for real: port 80 to `dmz-host` connected,
`servers-host` was unreachable.

`docker-demo-negative-control.txt` proves the checker isn't just printing
PASS by default. I pointed both `dmz` and `servers` at a host that's actually
reachable (`dmz-host`) with no `allowed_paths` entry, and the script
correctly reported two FAILs with exit code 1.

`docker-network-topology.txt` and `docker-containers.txt` are the supporting
`docker network inspect` / `docker ps` output confirming which container sat
on which network.

## What this demo does NOT prove

Docker bridge networks isolate by network membership, not by port — two
containers on the *same* bridge network can reach each other on any port,
there's no firewall between them. That's why `dmz-host` had to be genuinely
absent from `servers-net` to prove the `servers` block, rather than relying
on a port-level rule the way the real pfSense/nftables setup in
`walkthrough.md` does. The real VLAN lab will need to prove port-level
enforcement too (e.g. `users` can reach `dmz` on 443 but not on 22) — this
demo only proves whole-network isolation.

## Still to add

Once the VirtualBox/pfSense lab is actually built: real per-segment VM
output, a Wireshark capture of a blocked attempt, and updated
`segments.local.yaml`-based results replacing/supplementing this Docker demo.
