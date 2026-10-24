# Security Policy

## Scope

Neon Toolkit is a local diagnostics and utility project for Android and Termux. It is not intended to bypass device security, access other people's data, or test networks without permission.

## Reporting a concern

Please report suspected vulnerabilities privately to the repository maintainer through GitHub's private vulnerability reporting feature if it is enabled for this repository. If it is unavailable, contact the maintainer through the public GitHub profile and avoid posting exploit details or sensitive data in a public issue.

## Safe-use expectations

- Do not run unknown scripts as root.
- Do not include passwords, tokens, private keys, personal documents, or private diagnostic logs in issues.
- Only test network endpoints you own or are authorized to access.
- FilePilot is designed not to delete files automatically; always verify backup destinations.
- Android and Termux permission restrictions are expected and must not be bypassed by unsafe workarounds.
