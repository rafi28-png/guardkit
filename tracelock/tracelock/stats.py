"""Lightweight stats for tabular outputs, to catch silent corruption."""
import csv
from pathlib import Path


def csv_stats(path: Path) -> dict | None:
    if path.suffix.lower() != ".csv":
        return None
    try:
        with open(path, newline="", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            rows = list(reader)
    except OSError:
        return None
    if not rows:
        return {"rows": 0, "columns": 0, "empty_cells": 0, "empty_ratio": 1.0}
    header, data = rows[0], rows[1:]
    total = sum(len(r) for r in data) or 1
    empty = sum(1 for r in data for c in r if c.strip() == "")
    return {
        "rows": len(data),
        "columns": len(header),
        "empty_cells": empty,
        "empty_ratio": round(empty / total, 3),
    }
