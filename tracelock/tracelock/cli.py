"""CLI: tracelock run -- python3 pipeline.py input.csv cleaned.csv"""
import argparse
import json
import sys
import time
from pathlib import Path

from .hashing import snapshot
from .report import build_provenance, markdown_report
from .tracer import run_traced


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="tracelock")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run_p = sub.add_parser("run", help="Run a command and record provenance")
    run_p.add_argument("--workdir", default=".", help="Directory to watch (default: .)")
    run_p.add_argument("--out", default="provenance.lock.json")
    run_p.add_argument("--report", default="report.md")
    run_p.add_argument("command", nargs=argparse.REMAINDER,
                       help="Command to run, after --")
    args = parser.parse_args(argv)
    if args.cmd == "run":
        command = [c for c in args.command if c != "--"]
        if not command:
            parser.error("run requires a command after --")
        workdir = Path(args.workdir).resolve()
        before = snapshot(workdir)
        start = time.time()
        exit_code, traced, _used = run_traced(command, workdir)
        duration = time.time() - start
        after = snapshot(workdir)
        prov = build_provenance(command, exit_code, duration, before, after, traced, workdir)
        Path(args.out).write_text(json.dumps(prov, indent=2), encoding="utf-8")
        Path(args.report).write_text(markdown_report(prov), encoding="utf-8")
        print(f"Exit code: {exit_code}")
        print(f"Inputs: {[e['path'] for e in prov['inputs']]}")
        print(f"Outputs: {[e['path'] for e in prov['outputs']]}")
        if prov["alerts"]:
            print("Alerts:")
            for a in prov["alerts"]:
                print(f"  - {a}")
        else:
            print("Alerts: none")
        print(f"Wrote {args.out} and {args.report}")
        return exit_code
    return 0


if __name__ == "__main__":
    sys.exit(main())
