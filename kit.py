"""GuardKit dispatcher: one command to reach all seven tools.

Usage:
  python kit.py list
  python kit.py demo            # runs all seven proofs, writes SUITE_REPORT.md + .html
  python kit.py test            # runs suite smoke tests
  python kit.py web             # prints where to open the web app
  python kit.py check <file>    # unified: runs BOTH CheckFirst and SafeOffer, shows the higher score
  python kit.py selfcheck       # runs SecretScan on the suite itself (excluding the fake leaky example)
  python kit.py --version
  python kit.py semver-diff ... # forwards to that tool's CLI
  python kit.py tracelock ...
  python kit.py wattshift ...
  python kit.py shmpipe ...     # needs pyarrow; see shmpipe/README.md
  python kit.py safeoffer ...
  python kit.py checkfirst ...
  python kit.py secretscan ...

Each tool still works standalone from its own folder. This file
does NOT merge their code - it routes to them, BusyBox-style, so
the suite stays clean and each tool stays understandable alone.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

TOOLS = {
    "semver-diff": ("semver-diff", "semver_diff"),
    "tracelock": ("tracelock", "tracelock"),
    "wattshift": ("wattshift", "wattshift"),
    "shmpipe": ("shmpipe", "shmpipe"),
    "safeoffer": ("safeoffer", "safeoffer"),
    "checkfirst": ("checkfirst", "checkfirst"),
    "secretscan": ("secretscan", "secretscan"),
}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("list", "--help", "-h"):
        print("GuardKit - Verify before you trust, make pipelines faster, greener, reproducible.")
        print("\nTools:")
        print("  semver-diff  Behavioral breaking-change detector (Trust)")
        print("  tracelock    Zero-code provenance for pipelines (Efficiency)")
        print("  wattshift    Carbon-aware scheduler for batch jobs (Efficiency)")
        print("  shmpipe      Zero-copy shared-memory pipes via Arrow (Efficiency)")
        print("  safeoffer    Don't Pay Yet checker for jobs/loans/deals (Trust, Bengali+English)")
        print("  checkfirst   Check Before You Forward for messages (Trust, Bengali+English)")
        print("  secretscan   Scan for hardcoded secrets before pushing (Trust)")
        print("\n  python kit.py demo    Run all seven proofs")
        print("  python kit.py test    Run suite smoke tests")
        print("  python kit.py web     Show the web app location")
        print("  python kit.py check <file>   Check a message AND an offer at once")
        print("  python kit.py selfcheck      Scan this suite for real secrets before upload")
        print("  python kit.py <tool> <args...>   Forward to a tool (paths relative to that tool's folder)")
        print("\n  Web: open web/index.html - CheckFirst + SafeOffer in one app, with tabs.")
        return 0
    if argv[0] in ("--version", "-v"):
        print("GuardKit 0.6.5")
        return 0
    if argv[0] == "check":
        if len(argv) < 2:
            print("Usage: python kit.py check <file-with-message-or-offer>")
            return 2
        p = Path(argv[1])
        if not p.exists():
            print(f"Error: file not found: {argv[1]}")
            print("Check the path and try again — no verdict can be given for a missing file.")
            return 2
        text = p.read_text(encoding="utf-8", errors="ignore")
        if not text.strip():
            print("Empty file — nothing to check. A GREEN 0/100 would be misleading here.")
            return 2
        sys.path.insert(0, str(ROOT / "checkfirst"))
        sys.path.insert(0, str(ROOT / "safeoffer"))
        from checkfirst import check as cf_check
        from safeoffer import check as so_check
        cf, so = cf_check(text), so_check(text)
        print(f"CheckFirst (message): {cf['score']}/100 — {cf['verdict']}")
        for f in cf["flags"]:
            print(f"  - {f['reason_en']}")
        print(f"SafeOffer (offer): {so['score']}/100 — {so['verdict']}")
        for f in so["flags"]:
            print(f"  - {f['reason_en']}")
        best = cf if cf["score"] >= so["score"] else so
        print(f"\nHighest: {best['score']}/100 — {best['verdict']}")
        print(best["advice"])
        return 1 if best["score"] >= 60 else 0
    if argv[0] == "selfcheck":
        sys.path.insert(0, str(ROOT / "secretscan"))
        from secretscan import scan_path
        findings = []
        for p in sorted(ROOT.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or ".git" in p.parts:
                continue
            if p == ROOT / "secretscan" / "examples" / "leaky.py":
                continue  # fake example, intentionally leaky
            findings.extend(scan_path(p))
        if not findings:
            print("Selfcheck: CLEAN — no secrets found in the suite (excluding the fake leaky example).")
            print("Note: this does not check .env files — see SecretScan's .env warning below if you have one.")
            return 0
        print(f"Selfcheck: {len(findings)} finding(s) — check before uploading:")
        for f in findings:
            print(f"  {f['file']}:{f['line']} [{f['rule']}] {f['description']}")
        return 1
    if argv[0] == "demo":
        from demo_all import main as demo_main
        return demo_main()
    if argv[0] == "test":
        sys.path.insert(0, str(ROOT / "tests"))
        import test_suite
        test_suite.test_all_seven()
        print("Suite smoke tests: PASS")
        return 0
    if argv[0] == "web":
        print(f"Open this file in a browser: {ROOT / 'web' / 'index.html'}")
        print("It has two tabs: Check a Message (CheckFirst) and Check an Offer (SafeOffer).")
        print("No server, no install, no upload - checking happens in your browser.")
        return 0
    tool = argv[0]
    if tool not in TOOLS:
        print(f"Unknown tool: {tool}. Run: python kit.py list")
        return 2
    folder, module = TOOLS[tool]
    # Run the tool's module from its own folder, so its relative imports work.
    result = subprocess.run([sys.executable, "-m", module] + argv[1:], cwd=ROOT / folder)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
