# Security Policy

GuardKit includes trust and safety tools. That makes security — and honesty about limits — more important than usual.

## What GuardKit is NOT

- CheckFirst and SafeOffer are **pattern checkers, not fact-checkers, not legal advice, and not medical advice**. A green result does not prove something is legitimate or true.
- GuardKit does **not** verify forged documents, company registrations, or visa authenticity. Always verify with BMET, the embassy, the employer, or an official source you find yourself.

## Reporting a security issue

If you find a vulnerability in GuardKit itself (for example, a way the web app could leak pasted text, or a tool that executes untrusted code unsafely), please open a GitHub issue with "SECURITY:" in the title and a minimal reproduction, without including any real personal data.

Do NOT report a scam message as a "security issue" in GuardKit — instead, add it as a pattern contribution (see CONTRIBUTING.md, anonymized).

## Privacy by design

- The web app (`web/index.html`) checks in your browser only. Nothing is uploaded or stored by GuardKit.
- The Python CLIs read the file you give them and print a verdict. They do not send data anywhere.
- If you run GuardKit in a fork that *does* send data to a server, you must disclose that clearly in that fork — the upstream design is local-first.
