"""Command-line interface: python -m semver_diff compare OLD NEW"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from .differ import compare_files


def _git_show(ref: str, file_path: str, tmpdir: str, label: str) -> str:
    """Extract file_path at git ref into a temp file. Returns temp path."""
    result = subprocess.run(
        ["git", "show", f"{ref}:{file_path}"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"git show failed for {ref}:{file_path}\n{result.stderr}")
    out = Path(tmpdir) / f"{label}.py"
    out.write_text(result.stdout, encoding="utf-8")
    return str(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="semver-diff",
        description="Detect silent behavioral breaking changes between two versions.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    cmp_parser = sub.add_parser("compare", help="Compare two Python files")
    cmp_parser.add_argument("old", nargs="?", help="Old file path (or file path in git, with --old-ref)")
    cmp_parser.add_argument("new", nargs="?", help="New file path")
    cmp_parser.add_argument("--old-ref", help="Git ref for old version, e.g. v1.4.2")
    cmp_parser.add_argument("--new-ref", help="Git ref for new version, e.g. HEAD")
    cmp_parser.add_argument("--file", help="File path inside the repo when using --old-ref/--new-ref")
    cmp_parser.add_argument("--limit", type=int, default=200,
                            help="Max test cases per function (default 200)")

    args = parser.parse_args(argv)
    if args.cmd == "compare":
        if args.old_ref or args.new_ref:
            if not (args.old_ref and args.new_ref and args.file):
                parser.error("--old-ref, --new-ref and --file must be used together")
            with tempfile.TemporaryDirectory() as tmpdir:
                old_path = _git_show(args.old_ref, args.file, tmpdir, "old")
                new_path = _git_show(args.new_ref, args.file, tmpdir, "new")
                report = compare_files(old_path, new_path, limit_per_function=args.limit)
        else:
            if not (args.old and args.new):
                parser.error("compare requires OLD and NEW file paths")
            report = compare_files(args.old, args.new, limit_per_function=args.limit)
        print(report.summary())
        # Exit 1 when a breaking change is found, so CI can fail the PR.
        return 1 if report.divergences else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
