"""File hashing and directory snapshots."""
import hashlib
from pathlib import Path

IGNORE_NAMES = {"provenance.lock.json", "report.md", "trace.log"}
IGNORE_DIRS = {"__pycache__", ".git", ".venv"}


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]  # short, readable, enough for an MVP demo


def snapshot(workdir: Path) -> dict:
    """Map relative path -> {hash, size} for all files under workdir."""
    out = {}
    for p in sorted(workdir.rglob("*")):
        if not p.is_file():
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        rel = str(p.relative_to(workdir))
        if rel in IGNORE_NAMES:
            continue
        try:
            out[rel] = {"hash": file_hash(p), "size": p.stat().st_size}
        except OSError:
            continue
    return out
