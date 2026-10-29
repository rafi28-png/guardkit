"""Example of silent corruption: writes mostly empty values."""
import csv
import sys

outp = sys.argv[1]
with open(outp, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value"])
    for i in range(1, 6):
        w.writerow([i, ""])
print("Wrote corrupted output")
