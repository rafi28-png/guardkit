# GuardKit Audit — 2026-10-30 (v0.6.1 check, updated v0.6.2)

## v0.6.2 — Edge-case audit (new)

Checked: missing/empty files, /tmp hardcoding, XSS, accessibility, dead imports.

**Found and fixed:**
- `kit.py check` on a missing file → ugly traceback. Now: "Error: file not found", exit 2.
- `kit.py check` on an empty file → misleading GREEN 0/100. Now: "Empty file — nothing to check", exit 2.
- Demo WattShift used `/tmp/gk_ws.*` and ShmPipe benchmark used `/tmp/shmpipe-bench` — breaks Windows/macOS and pollutes /tmp. Now both use `tempfile`.
- Unused imports: `math` in semver-diff inputs, `traceback` in semver-diff runner, `os` in shmpipe test. Removed (both guardkit and standalone).
- Web accessibility: no noscript, no aria, labels without `for=`, no focus outline. Added noscript message, aria-labels, `for="msg"` / `for="offer"`, focus-visible outline.

**Checked, no change needed:**
- XSS: web `innerHTML` uses only code-controlled strings (scores, rule reasons, verdicts, dates) — user pasted text is never inserted via innerHTML (it goes via `value` / `textContent`). Safe as-is.
- Standalone sync after fixes: still 0 differences for all 7 tools.

**New tests:** punycode, work-permit fee, Bengali examples (100/100), .env warning, kit check missing/empty — all in `tests/test_suite.py`.

**One-command check:** `sh check_all.sh` runs demo + suite tests + selfcheck + per-tool pytest.

Checked more, not just demo + tests. Method: version check, CLI help for all 7 tools, pyproject TOML validation, markdown link check, secret scan, web JS logic test with a mocked DOM, standalone vs suite diff, file size / empty dir check.

## What passed (no action needed)

- **Demo:** ALL PASS (7/7), selfcheck CLEAN
- **Tests:** 16 pytest tests pass across all 7 tools, from their own folders
- **CLI help:** all 7 tools show correct help (`compare`, `run`, `advise`, `write/read/cat/top/rm`, `check`, `check`, `scan`)
- **TOML:** all pyproject.toml files parse OK
- **Markdown links:** no broken `[text](file)` links found (earlier "broken" hits were plain text, not links)
- **File size:** 109 files, 524 KB total, no file over 100 KB — safe for GitHub web upload
- **Web logic (mocked DOM test):**
  - Live preview message "Send OTP + bit.ly + lottery" → 70/100, 3 flags, RED on Check
  - Live preview offer "tourist visa + cash no receipt + passport kept" → 85/100, 3 flags, RED on Check
  - Verdicts from live preview and full Check match
- **Secrets:** selfcheck CLEAN, excluding the intentional fake leaky example

## Issues found and fixed in v0.6.1

1. **SecretScan had no pyproject.toml** — every other tool had one. Added it (same format, version 0.1.0, MIT).
2. **Standalone copies were out of sync** — guardkit/checkfirst, safeoffer, and secretscan had newer patterns / examples / .env check than ~/workspace/checkfirst, safeoffer, secretscan. Fixed by copying: CheckFirst punycode rule + bangla_scam.txt, SafeOffer work-permit-fee rule + bangla_fake_job.txt, SecretScan .env check (__init__ + cli) + pyproject.toml. Re-diff after fix: **0 differences** for all 7 tools.
3. **Empty directory `safeoffer/data/`** — empty folders are not tracked by git and confuse upload. Removed (in both guardkit and standalone).
4. **False positives ruled out:**
   - `TODO` in checkfirst/app.js is a variable name for "what to do" list, not a placeholder task.
   - Earlier "broken link" hits were plain text mentions, not markdown links.

## Intentional differences (not bugs)

- Standalone CheckFirst / SafeOffer web apps are single-tool apps; guardkit/web is the combined app with tabs, history, gauges, and chips. They are not supposed to be identical.
- Subproject versions are all 0.1.0; suite version is 0.6.1. Suite version tracks the suite, not each tool.

## How to re-run this audit

```bash
python kit.py demo
python kit.py selfcheck
# from each tool folder:
python -m pytest tests/ -q
```
