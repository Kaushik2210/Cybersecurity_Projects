# Day 03 — Notes

## What I learned
<!-- Fill in after doing the Wireshark side: what the TLS ClientHello/SNI
     actually looked like in the packet details, anything that surprised you
     comparing curl's numbers to the script's. -->

## What broke and how I fixed it
<!-- Fill in as you hit real issues — e.g. a captive portal or corporate
     proxy intercepting TLS and changing what the certificate shows. -->

## Interview questions someone could ask me about this
1. Q: Why measure DNS, TCP, and TLS as separate phases instead of one total time?
   A: Each layer fails or slows for different reasons — DNS problems point to
   resolver/domain issues, TCP delays point to network path issues, TLS
   delays point to certificate or negotiation problems. A single total time
   can't tell you which layer to investigate.

2. Q: What is SNI and why does it matter for privacy/security?
   A: It's the hostname the client sends, unencrypted, at the start of the
   TLS handshake so the server knows which certificate to present. Because
   it's unencrypted, anyone observing the network can see which hostname
   you're connecting to even over HTTPS.

3. Q: Why did the script use the default certificate-verifying TLS context instead of disabling verification?
   A: Disabling verification defeats the purpose of TLS — it would accept a
   certificate from an attacker performing a machine-in-the-middle attack.
   The default, verifying context is what any real HTTP client should use.

4. Q: What would a misconfigured or malicious TLS endpoint look like in a packet capture?
   A: A certificate subject that doesn't match the requested SNI hostname, an
   unexpectedly outdated TLS version, or a self-signed certificate where a
   public CA-issued one is expected.
