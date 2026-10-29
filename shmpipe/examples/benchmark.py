"""Benchmark: CSV write+read vs ShmPipe write+read, same data.

Usage: python examples/benchmark.py [rows]
Default 1,000,000 rows. Prints timings and speedup, no claims beyond
what was actually measured on this machine.
"""
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pyarrow as pa
import pyarrow.csv as pa_csv

from shmpipe import read_table, write_table

ROWS = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
TMP = Path(tempfile.mkdtemp(prefix="shmpipe-bench-"))
CSV_PATH = TMP / "data.csv"
OUT_CSV = TMP / "out.csv"


def make_table(n):
    return pa.table({
        "id": list(range(n)),
        "value": [float(i % 1000) / 10 for i in range(n)],
        "label": [f"row-{i % 100}" for i in range(n)],
    })


def timeit(fn):
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


def main():
    print(f"Generating {ROWS:,} rows...")
    table = make_table(ROWS)

    csv_time = timeit(lambda: (
        pa_csv.write_csv(table, str(CSV_PATH)),
        pa_csv.read_csv(str(CSV_PATH)),
    ))
    print(f"CSV write + read: {csv_time:.3f}s  (file {CSV_PATH.stat().st_size/1e6:.1f} MB)")

    shm_time = timeit(lambda: (
        write_table("bench", table),
        read_table("bench"),
    ))
    print(f"ShmPipe write + read: {shm_time:.3f}s")
    if shm_time > 0:
        print(f"Speedup: {csv_time/shm_time:.1f}x faster than CSV")
        print(f"CSV time / ShmPipe time = {csv_time:.3f} / {shm_time:.3f}")

    # Correctness check: round-trip must preserve rows
    back = read_table("bench")
    assert back.num_rows == ROWS, (back.num_rows, ROWS)
    print(f"Round-trip check: OK ({back.num_rows:,} rows preserved)")


if __name__ == "__main__":
    main()
