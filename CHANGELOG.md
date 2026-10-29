# Changelog

## 0.6.5 — OSS application plan (2026-10-30)
- Added docs/OSS_APPLICATIONS.md: honest checklist against Claude for OSS and Codex for OSS, with draft application texts (under 500 chars, no inflated numbers).
- Fixed PyPI readiness: SemVer-Diff pyproject was missing license/authors/classifiers; SecretScan now has classifiers + console script. Both synced to standalone copies.
- No code behaviour changed; demo still ALL PASS.

## 0.6.4 — Again: LICENSE per tool, honest SKIPPED, WhatsApp share (2026-10-30)
- Fixed: no LICENSE file in any standalone tool folder (only top-level). Added MIT LICENSE to all 7 tools, in guardkit and standalone copies.
- Fixed: .gitignore missing in 6 of 7 tools. Added __pycache__ / *.pyc / .pytest_cache to all.
- Fixed: demo called a skipped ShmPipe "PASS (exit None)". Now it says "SKIPPED" and overall is "ALL PASS (1 skipped)" — honest, not inflated.
- Added: WhatsApp share button for CheckFirst verdicts (opens wa.me with the share text), and Clear buttons for both tabs.
- Checked: py_compile on all Python files OK, long input (10k chars) scores in 0.002s, binary-like input does not crash.
- All 16 pytest tests pass + demo ALL PASS + selfcheck CLEAN. Now 128 files (7 LICENSE + 6 .gitignore + web changes).

## 0.6.3 — Again: Bengali completeness, naming, VM path, legit examples (2026-10-30)
- Fixed: Bengali UI was incomplete — live preview, advice, share text, and history empty message stayed English in Bengali mode. Now all translated.
- Fixed: test was still called test_all_six for seven tools. Renamed to test_all_seven, with test_all_six kept as an alias. kit.py and CI updated.
- Fixed: demo_all.py hardcoded /tmp/shm_venv/bin/python (a VM-only path). Now uses current Python, with optional GUARDKIT_SHMPIPE_PYTHON override.
- Added: Bengali legit example (0/100 GREEN) and worldwide legit example (20/100 GREEN) — proves legit messages/offers are not flagged, in any language.
- Added: docs/EXAMPLES.md — every example with its expected score, in one table.
- All tests pass + demo ALL PASS + selfcheck CLEAN.

## 0.6.2 — Edge-case audit, better (2026-10-30)
- Fixed: kit.py check on missing file gave an ugly traceback — now a friendly error, exit 2. Empty file gave misleading GREEN 0/100 — now "Empty file, nothing to check", exit 2.
- Fixed: demo_all.py WattShift and ShmPipe benchmark used hardcoded /tmp — now tempfile, so demo works on Windows/macOS too.
- Fixed: unused imports removed (semver-diff inputs/runner, shmpipe test).
- Added: tests for new patterns (punycode, work-permit fee), Bengali examples, .env warning, and kit check missing/empty cases — suite tests now cover those.
- Added: check_all.sh (demo + tests + selfcheck in one command), web noscript message, aria-labels, label for=, focus-visible outline.
- Checked XSS: web innerHTML uses only code-controlled strings (scores, rule text, verdicts) — no user text is inserted via innerHTML. No change needed, documented in docs/AUDIT.md.
- All 16 pytest tests pass + demo ALL PASS + selfcheck CLEAN, standalone sync still 0 differences.

## 0.6.1 — Deep audit, fixes (2026-10-30)
- Checked more at Tiara's request: versions, CLI help, TOML, links, secrets, web JS logic (mocked DOM), standalone vs suite diff, file sizes
- Fixed: SecretScan missing pyproject.toml; standalone copies out of sync (CheckFirst/SafeOffer/SecretScan); empty safeoffer/data/ removed
- Verified web logic: live preview 70/100 (message) and 85/100 (offer), verdicts match full Check
- Full audit report in docs/AUDIT.md. No broken markdown links, no file over 100 KB, 109 files, 524 KB total

## 0.6.0 — Visually stunning, interactive (2026-10-30)
- Web app redesign: gradient hero, glass-like cards, animated score gauge (bar grows on check), pulsing RED card, hover lift, dark mode improved, mobile-first
- Interactive: live risk preview as you type (before pressing Check), clickable example chips (OTP, lottery, bit.ly, tourist visa, cash no receipt, passport kept)
- Landing page: interactive tool explorer — filter by Trust / Efficiency, live search, click any tool card to expand a tip
- SUITE_REPORT.html redesigned to match: gradient hero, rounded table, worldwide badge
- Worldwide positioning kept: English primary, Bengali supported, not Bengali-only

## 0.5.1 — Worldwide repositioning (2026-10-30)
- Correction at Tiara's request: GuardKit is NOT a Bengali-only project. It is worldwide, English primary.
- Bengali remains as a supported language for CheckFirst / SafeOffer (verdicts, questions, examples), not as the project's identity.
- Updated main README, web intro, landing page, and README_BN header to say this clearly. No tools removed, no Bengali support removed — only the positioning was fixed.
- Translations for other languages welcome — see CONTRIBUTING.md.

## 0.5.0 — Unified check, selfcheck, Bengali examples, GitHub templates (2026-10-30)
- New `kit.py check <file>`: runs BOTH CheckFirst and SafeOffer, shows the higher score — for users who don't know which tab to use
- New `kit.py selfcheck`: SecretScan on the suite itself, excluding the fake leaky example. Now CLEAN after fixing SecretScan's own docstring, which mentioned an example AWS key and flagged itself
- New Bengali examples: CheckFirst bangla_scam (100/100 RED), SafeOffer bangla_fake_job (100/100 RED)
- SecretScan: new .env gitignore warning — if a .env exists but .gitignore doesn't list .env, warn before committing (without printing values)
- Added GitHub issue templates (scam pattern, bug), PR template, CODE_OF_CONDUCT.md, README badges, and README_BN.md (Bengali summary)
- All 16 pytest tests pass + demo ALL PASS + selfcheck CLEAN

## 0.4.0 — Full Bengali UI option, new patterns, landing page (2026-10-30)
- Web app: full Bengali UI (not just verdicts), Bengali SafeOffer questions, dark mode with saved preference, mobile full-width buttons, print style
- New patterns: CheckFirst punycode (xn--) + IP-link + account-closed threats; SafeOffer work-permit / medical / training fees. Old examples unchanged: scam still 100/100, fake job still 100/100
- Added web/landing.html for GitHub Pages, and install.sh (checks Python, optionally installs pyarrow, runs demo)
- All 16 pytest tests pass across the seven tools, plus suite demo ALL PASS

## 0.3.1 — Test fix + upload guide (2026-10-30)
- Fixed TraceLock tests: command string was passed as one filename, so pytest always failed. Tool was correct, test was wrong. Now all tools pass under pytest from their own folders.
- Added UPLOAD_TO_GITHUB.md (no-coding, web-upload guide, including GitHub Pages), docs/architecture.svg, docs/FAQ.md + Roadmap
- Note: system Python has no pytest (externally managed); use a venv with pytest, as documented in the FAQ

## 0.3.0 — Seven tools, HTML report, better web app (2026-10-30)
- New 7th tool: SecretScan — scan for hardcoded secrets before pushing, with redacted output and `# secretscan:ignore`
- Demo now writes SUITE_REPORT.html as well as SUITE_REPORT.md
- Web app: local-only history of last 5 checks, plus link-domain display for messages
- kit.py now routes to secretscan, version bumped to 0.3.0

## 0.2.0 — Improved suite (2026-10-30)
- Added LICENSE (MIT), CONTRIBUTING.md, SECURITY.md, .gitignore, requirements.txt
- Added suite CI workflow (`.github/workflows/suite.yml`) that runs `kit.py demo` and smoke tests on every PR
- Added `kit.py test` and `kit.py web` commands, and `kit.py --version`
- Web app now showcases all six tools, not just the two trust tabs, and re-checks when you switch language
- SUITE_REPORT.md is now generated by the demo and kept as proof in the repo

## 0.1.0 — Initial suite (2026-10-30)
- Six tools in one monorepo: SemVer-Diff, TraceLock, WattShift, ShmPipe, SafeOffer, CheckFirst
- `kit.py` dispatcher, `demo_all.py` (now `kit.py demo`), combined CheckFirst + SafeOffer web app
- Demo result: ALL PASS
