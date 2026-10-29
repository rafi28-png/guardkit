"""Build provenance.lock.json and a Markdown report with a Mermaid DAG."""
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from .stats import csv_stats


def build_provenance(command, exit_code, duration_s, before, after,
                     traced, workdir: Path) -> dict:
    inputs, outputs = [], []
    for rel, info in after.items():
        entry = {"path": rel, "hash": info["hash"], "size": info["size"]}
        stats = csv_stats(workdir / rel)
        if stats:
            entry["csv_stats"] = stats
        if rel not in before:
            outputs.append(entry)
        elif before[rel]["hash"] != info["hash"]:
            outputs.append(entry)
        elif rel in traced:
            inputs.append(entry)

    # Files read by strace but unchanged are also inputs, even if
    # they were not in the after-snapshot logic above.
    known = {e["path"] for e in inputs + outputs}
    for rel in traced:
        if rel in known or rel not in before:
            continue
        info = before[rel]
        entry = {"path": rel, "hash": info["hash"], "size": info["size"]}
        stats = csv_stats(workdir / rel)
        if stats:
            entry["csv_stats"] = stats
        inputs.append(entry)

    alerts = []
    input_rows = None
    for e in inputs:
        if e.get("csv_stats"):
            input_rows = e["csv_stats"]["rows"]
    for e in outputs:
        s = e.get("csv_stats")
        if not s:
            continue
        if s["rows"] == 0:
            alerts.append(f"{e['path']}: output is empty (0 rows)")
        if s["empty_ratio"] >= 0.5:
            alerts.append(f"{e['path']}: {s['empty_ratio']*100:.0f}% empty cells - possible silent corruption")
        if input_rows and s["rows"] < 0.5 * input_rows:
            alerts.append(f"{e['path']}: row count dropped from {input_rows} to {s['rows']}")

    return {
        "tool": "tracelock",
        "version": "0.1.0",
        "command": command,
        "exit_code": exit_code,
        "duration_seconds": round(duration_s, 3),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "inputs": sorted(inputs, key=lambda x: x["path"]),
        "outputs": sorted(outputs, key=lambda x: x["path"]),
        "traced_files": sorted(traced),
        "alerts": alerts,
    }


def mermaid(provenance: dict) -> str:
    lines = ["```mermaid", "flowchart LR"]
    for i, e in enumerate(provenance["inputs"]):
        lines.append(f'    in{i}["{e["path"]}"]')
    lines.append(f'    cmd["{provenance["command"][0]}"]')
    for i, e in enumerate(provenance["outputs"]):
        lines.append(f'    out{i}["{e["path"]}"]')
    for i in range(len(provenance["inputs"])):
        lines.append(f"    in{i} --> cmd")
    for i in range(len(provenance["outputs"])):
        lines.append(f"    cmd --> out{i}")
    lines.append("```")
    return "\n".join(lines)


def markdown_report(provenance: dict) -> str:
    lines = [
        "# TraceLock Report",
        "",
        f"**Command:** `{' '.join(provenance['command'])}`",
        f"**Exit code:** {provenance['exit_code']}  |  **Duration:** {provenance['duration_seconds']}s",
        "",
        "## Lineage",
        "",
        mermaid(provenance),
        "",
        "## Inputs",
        "",
    ]
    for e in provenance["inputs"] or [{"path": "(none detected)"}]:
        lines.append(f"- `{e['path']}` hash `{e.get('hash', '')}` {e.get('size', '')} bytes {e.get('csv_stats', '')}")
    lines += ["", "## Outputs", ""]
    for e in provenance["outputs"] or [{"path": "(none detected)"}]:
        lines.append(f"- `{e['path']}` hash `{e.get('hash', '')}` {e.get('size', '')} bytes {e.get('csv_stats', '')}")
    lines += ["", "## Alerts", ""]
    if provenance["alerts"]:
        for a in provenance["alerts"]:
            lines.append(f"- ⚠️ {a}")
    else:
        lines.append("- No alerts. No empty outputs, no major row-count drop, no high missingness detected.")
    return "\n".join(lines) + "\n"
