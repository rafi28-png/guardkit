# GuardKit — Verify Before You Trust. Make Pipelines Faster, Greener, Reproducible.

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Tools: 7](https://img.shields.io/badge/Tools-7-orange.svg)
![Worldwide](https://img.shields.io/badge/Worldwide-English%20primary-green.svg)
![Bengali supported](https://img.shields.io/badge/Bengali-supported-blue.svg)

**GuardKit is a worldwide project, not a Bengali-only project.** English is the primary language for the whole suite — docs, code, web app, and verdicts. Bengali support is an *additional* language for CheckFirst and SafeOffer (verdicts, questions, and examples), because some of the fraud patterns were first documented in Bangladesh, but the patterns themselves — OTP scams, lottery scams, tourist-visa jobs, cash with no receipt, passport kept — apply worldwide. Translations for other languages are welcome (see CONTRIBUTING.md).

**Bengali summary (translation only, not the main README): [README_BN.md](README_BN.md)**

**Version 0.6.5 — One suite, seven working tools, built in one day — each still usable alone.**

**What's new in 0.6.4:** LICENSE + .gitignore in every tool folder, honest SKIPPED display in the demo, WhatsApp share + Clear buttons in the web app.

**What's new in 0.6.3:** Bengali UI completed (advice, live preview, history), test renamed to seven, VM-only demo path removed, Bengali legit + worldwide legit examples, and docs/EXAMPLES.md with every expected score.

**What's new in 0.6.2:** Edge-case fixes — friendly errors for missing/empty files, no more /tmp hardcoding, accessibility (noscript, aria, focus), and new tests. One-command check: `sh check_all.sh`. See docs/AUDIT.md.

**What's new in 0.6.1:** Deep audit — see [docs/AUDIT.md](docs/AUDIT.md). Fixed SecretScan pyproject, standalone sync, and empty dir. Web logic tested with mocked DOM.

**What's new in 0.6.0:** Visually stunning, interactive web app — gradient hero, animated score gauge, live risk preview as you type, clickable example chips, interactive landing page with tool filter + search. See CHANGELOG.md. Worldwide, English primary, Bengali supported.

**What's new in 0.5.0:** `kit.py check <file>` (both trust checkers at once), `kit.py selfcheck` (suite is CLEAN), Bengali examples that both score 100/100 RED, SecretScan .env gitignore warning, GitHub issue/PR templates, CODE_OF_CONDUCT, and a Bengali README. See CHANGELOG.md.

**Quick check, no tab choice needed:**
```bash
python kit.py check checkfirst/examples/bangla_scam.txt
python kit.py selfcheck
```

**Uploading to GitHub with no coding experience?** See [UPLOAD_TO_GITHUB.md](UPLOAD_TO_GITHUB.md) — web-upload steps, GitHub Pages, and what to write in your submission.

**What's new in 0.5.1:** Worldwide repositioning — English is primary, Bengali is a supported language, not the project's identity. No tools were removed; Bengali examples and translations remain as support, not as the main story. See CHANGELOG.md.

**What's new in 0.3.0:** New 7th tool SecretScan (scan for hardcoded secrets before pushing), HTML suite report (`SUITE_REPORT.html` alongside `.md`), web app history (local only) + link-domain display, and updated docs. See CHANGELOG.md for details.

GuardKit is not one giant merged program. It's a BusyBox-style suite: each tool keeps its own folder, its own README, and its own tests, and one dispatcher ties them together. That way the suite looks heavy, but no tool loses its clarity.

## The seven tools

### Trust — verify before you trust

| Tool | What it does in one line | Try it |
|---|---|---|
| **SemVer-Diff** (`semver-diff/`) | Catches silent behavioral breaking changes in a "safe" patch, even with no tests | `python kit.py semver-diff compare examples/old/math_utils.py examples/new/math_utils.py` (paths are relative to the tool's folder, because kit forwards to it) |
| **CheckFirst** (`checkfirst/`) | Paste a forwarded message, get a plain-language scam / misinformation check, in English (Bengali supported) | Open `web/index.html`, tab "Check a Message" |
| **SafeOffer** (`safeoffer/`) | Paste a job / loan / deal offer before you pay, get a "Don't Pay Yet" check, in English (Bengali supported) | Open `web/index.html`, tab "Check an Offer" |
| **SecretScan** (`secretscan/`) | Scan a file/folder for hardcoded AWS, GitHub, Slack tokens, private keys, passwords — before you push | `python kit.py secretscan scan examples/leaky.py` |

### Efficiency — pipelines

| Tool | What it does in one line | Try it |
|---|---|---|
| **TraceLock** (`tracelock/`) | Wrap any pipeline unchanged, get input/output hashes, CSV health alerts, and a Mermaid lineage diagram | `python kit.py tracelock run -- python3 pipeline.py raw.csv cleaned.csv` (in tracelock demo folder) |
| **WattShift** (`wattshift/`) | Find the cleanest time to run a batch job inside your deadline, with CO2 saved and a README badge | `python kit.py wattshift advise --max-delay-hours 4 --duration-minutes 60 --energy-kwh 2` |
| **ShmPipe** (`shmpipe/`) | Pass Arrow tables between processes via shared memory, instead of CSV to disk and back | `python examples/benchmark.py 5000000` (needs pyarrow) |

## One command to prove it all works

```bash
python kit.py list
python kit.py demo
```

`demo` runs all seven proofs with their own examples and writes `SUITE_REPORT.md` + `SUITE_REPORT.html`. It does not claim results — it runs them and records exit codes and output.

**Measured results from the suite demo (this machine, reproducible examples):**

- SemVer-Diff: 3 functions, 88 cases, **4 divergences** — breaking change found, exit 1
- TraceLock: good pipeline, inputs `[pipeline.py, raw.csv]`, outputs `[cleaned.csv]`, **Alerts: none**; corrupt pipeline alerts on 50% empty cells
- WattShift: reproducible forecast — run now 290 gCO2/kWh, best in 4h 115 gCO2/kWh, **saved 350g CO2 (60.3%)** for 2 kWh; live UK API run saved 73g (33.3%)
- ShmPipe: 5,000,000 rows — CSV 2.031s, ShmPipe 0.306s, **6.6x faster** (1M rows: 3.7x). Honest note: less than the hoped-for 20x, because Arrow's CSV reader is already fast.
- SafeOffer: fake job **100/100 RED — DO NOT PAY YET**, loan scam 90/100 RED, legit example 20/100 GREEN
- CheckFirst: scam forward **100/100 RED — DO NOT FORWARD**, health rumor 70/100 RED, legit example 0/100 GREEN
- SecretScan: leaky example **3 findings** (AWS, GitHub, password), clean example **0 findings**

If pyarrow is not installed, ShmPipe is reported as SKIPPED in the suite report, not as a failure — install with `pip install pyarrow` to run it.

## Web app

Open `web/index.html` in any browser, on a phone is fine. Two tabs, one app:

- **Check a Message** (CheckFirst rules)
- **Check an Offer** (SafeOffer rules)

Checking happens in your browser. Nothing is uploaded, nothing is stored. Never paste OTP, passwords, passport, or bank details — paste the message / offer, not your identity.

## Install / use alone

Each folder is a standalone project with its own README and `pyproject.toml`. You can copy any single folder to GitHub on its own and it works — the suite does not break that.

```bash
# Example: use only CheckFirst
cd checkfirst && python -m checkfirst check examples/scam_forward.txt
# Example: use only SemVer-Diff
cd semver-diff && python -m semver_diff compare examples/old/math_utils.py examples/new/math_utils.py
```

## Honest limits (for the whole suite)

- These are MVPs, not finished products. Each README lists its own limits: e.g. SemVer-Diff is Python pure functions only, TraceLock is Linux + strace for full tracing, WattShift live data is UK API only, ShmPipe's R helper was not tested here (R not installed), CheckFirst / SafeOffer flag patterns — they do not prove truth or legitimacy, and they are not legal or medical advice.
- Always verify officially: BMET / embassy / employer for offers, official sources for messages, and your own tests for code changes.

## Layout

```
guardkit/
  README.md, kit.py, demo_all.py, SUITE_REPORT.md + SUITE_REPORT.html (generated by demo)
  web/                 # Combined CheckFirst + SafeOffer web app, with history
  semver-diff/ tracelock/ wattshift/ shmpipe/ safeoffer/ checkfirst/ secretscan/
  tests/test_suite.py
```

## License

MIT — each subproject is MIT as well.
