"""Run a command and trace what it reads and writes.

Primary method on Linux: strace -f, filtered to files under the workdir.
Fallback: before/after snapshot diff (works anywhere, no root needed).
"""
import re
import shutil
import subprocess
from pathlib import Path

_OPEN_RE = re.compile(r'openat\(AT_FDCWD,\s*"([^"]+)"')


def parse_strace(trace_path: Path, workdir: Path) -> list:
    seen = []
    if not trace_path.exists():
        return seen
    for line in trace_path.read_text(errors="ignore").splitlines():
        m = _OPEN_RE.search(line)
        if not m:
            continue
        raw = m.group(1)
        p = Path(raw)
        if not p.is_absolute():
            p = workdir / p
        try:
            rel = str(p.resolve().relative_to(workdir.resolve()))
        except ValueError:
            continue  # system file, outside the project - ignore
        if rel in (".", ""):
            continue
        if (workdir / rel).is_dir():
            continue
        if rel not in seen and rel not in ("provenance.lock.json", "report.md", "trace.log"):
            seen.append(rel)
    return seen


def run_traced(command: list, workdir: Path):
    """Run command, return (exit_code, traced_files, strace_used)."""
    strace = shutil.which("strace")
    trace_path = workdir / "trace.log"
    if strace:
        full = [strace, "-f", "-e", "trace=openat,open,creat",
                "-o", str(trace_path)] + command
        result = subprocess.run(full, cwd=workdir)
        traced = parse_strace(trace_path, workdir)
        try:
            trace_path.unlink()
        except OSError:
            pass
        return result.returncode, traced, True
    result = subprocess.run(command, cwd=workdir)
    return result.returncode, [], False
