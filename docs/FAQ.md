# GuardKit FAQ

**Do I need to install anything to try the web app?**
No. Open `web/index.html` in a browser. It works offline, in English and Bengali, and nothing is uploaded.

**Do I need Python to use all seven tools?**
Yes for the command-line tools, Python 3.9+. Five tools need no extra install. ShmPipe needs `pip install pyarrow`.

**Is a GREEN result proof something is safe / true?**
No. CheckFirst and SafeOffer flag patterns. Green means "no major flags found on these checks only". Always verify officially.

**Why is ShmPipe sometimes SKIPPED in the demo?**
If pyarrow is not installed in that Python, the demo reports it as SKIPPED, not as a failure, so the report stays honest.

**Can I use one tool alone, without the suite?**
Yes. Copy that tool's folder alone — each has its own README, tests, and `pyproject.toml`.

**What was fixed in v0.3.1?**
TraceLock's tests had a bug: the test passed a whole command string as one filename, so pytest always failed. Fixed by splitting the command (`*script.split()`). The tool itself was correct — the test was wrong. All tools now pass under pytest when run from their own folders.

# Roadmap (not promises)

- CheckFirst: image / reverse-image guidance as a real check, not just advice
- SafeOffer: official verification links per country, starting with Bangladesh (BMET)
- WattShift: more regions beyond UK carbon data
- SecretScan: git-history scanning guidance (use gitleaks/trufflehog for history, SecretScan for working files)
- GuardKit web: dark mode, and a printable one-page checklist
