# Contributing to GuardKit

Thank you for helping make GuardKit better — especially for the trust tools, where a wrong verdict can hurt a real person.

## How to contribute (no coding experience needed)

- **Report a missed scam / offer pattern:** Open an issue with the message text (remove all personal details, OTPs, bank details, and names first) and what GuardKit said vs what it should have said.
- **Add a pattern:** Rules live in `checkfirst/checkfirst/checker.py`, `safeoffer/safeoffer/checker.py`, and the web apps in `web/app.js`. Each rule needs: a pattern, a plain-language reason in English, and the same reason in Bengali if you can (Bengali is supported, not required).
- **Add a translation:** GuardKit is worldwide, English primary. To add another language, translate the verdicts and questions in `web/app.js` and the `reason_en` fields in the Python checkers, keeping English as the fallback. Do not replace English — add alongside it.
- **Fix a false positive:** If a legit message/offer is marked red, that's a bug. Include the example (anonymized) and the expected verdict.

## For code changes

1. Keep each tool standalone — do not make one tool depend on another, except through `kit.py`.
2. Every new rule needs a test in that tool's `tests/` folder, with a fake example and a legit example.
3. Run the suite proof before opening a PR:
   ```bash
   python kit.py demo
   python -c "import sys; sys.path.insert(0, 'tests'); import test_suite; test_suite.test_all_six(); print('PASS')"
   ```
4. Do not add a new dependency without explaining why in the PR, and keep ShmPipe's `pyarrow` optional — the trust tools must work with Python's standard library only.

## Safety rules (non-negotiable)

- Never ask for, store, or log OTPs, passwords, passport numbers, or bank details.
- Never claim 100% certainty for CheckFirst / SafeOffer. Say "suspicious, here's why" and direct people to official verification.
- Never use a real person's message as a test example without anonymizing it completely.
