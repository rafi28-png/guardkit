"""CLI: python -m checkfirst check <file>  OR  echo text | python -m checkfirst check -"""
import argparse
import json
import sys

from .checker import check


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="checkfirst")
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="Check a message file, or - for stdin")
    c.add_argument("path")
    c.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "check":
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        result = check(text)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Score: {result['score']}/100")
            print(f"Verdict: {result['verdict']}  ({result['verdict_bn']})")
            print(f"Advice: {result['advice']}")
            print("\nFlags found:")
            for f in result["flags"] or [{"reason_en": "(none)"}]:
                print(f"  - [{f.get('level', '')}] {f['reason_en']}")
            print("\nWhat to do:")
            for step in result["what_to_do"]:
                print(f"  - {step}")
            print(f"\nShare: {result['share_text']}")
            print(f"\n{result['disclaimer']}")
        return 1 if result["score"] >= 60 else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
