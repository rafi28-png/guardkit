"""CLI: python -m secretscan scan <path> [--json]"""
import argparse
import json
import sys
from pathlib import Path

from .scanner import check_env_gitignore, scan_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="secretscan")
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="Scan a file or folder for hardcoded secrets")
    s.add_argument("path", default=".")
    s.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "scan":
        findings = scan_path(Path(args.path))
        for w in check_env_gitignore(Path(args.path)):
            print(f"WARNING: {w}")
        if args.json:
            print(json.dumps(findings, indent=2))
        else:
            if not findings:
                print("No secrets found. (This does not prove there are none - check .env files are gitignored.)")
            else:
                print(f"Found {len(findings)} potential secret(s) - check before pushing:")
                for f in findings:
                    print(f"  {f['file']}:{f['line']} [{f['rule']}] {f['description']} -> {f['redacted']}")
                print("\nFix: move the value to an environment variable, rotate it if it was ever pushed, and add the file to .gitignore.")
        return 1 if findings else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
