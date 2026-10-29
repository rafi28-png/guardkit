"""Example pipeline: read raw.csv, drop empty rows, write cleaned.csv."""
import csv
import sys

inp, outp = sys.argv[1], sys.argv[2]
with open(inp, newline="") as f:
    rows = [r for r in csv.DictReader(f) if any(v.strip() for v in r.values())]
with open(outp, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "value"])
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {len(rows)} rows to {outp}")
