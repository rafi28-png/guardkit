# ShmPipe

**Stop paying the CSV tax every time data moves between tools.**

Unix pipes pass text. When a Python script hands a table to R, or to another Python process, the usual path is: write a CSV to disk, then parse that text back into memory. On large tables most of the time is that round-trip, not the actual work.

ShmPipe instead writes an Apache Arrow table once to shared memory (`/dev/shm`, which is RAM on Linux), and the next process opens it memory-mapped — no CSV, no disk, no re-parsing.

```python
import shmpipe
shmpipe.write_table("demo", my_table)   # producer
table = shmpipe.read_table("demo")      # consumer, in another process
```

## CLI demo

```bash
shmpipe write demo data.csv
shmpipe top
shmpipe cat demo | grep 20      # classic Unix fallback still works
shmpipe read demo out.csv
shmpipe rm demo
```

Real output from this project:

```
Wrote 3 rows, 432 bytes to shared memory as 'demo'
NAME  ROWS  SIZE  COLUMNS
demo     3   432  id,value
```

## Real benchmark (measured, not claimed)

Run it yourself:

```bash
python examples/benchmark.py 5000000
```

Measured on this machine, 5,000,000 rows, 106.9 MB as CSV:

```
CSV write + read: 2.031s
ShmPipe write + read: 0.306s
Speedup: 6.6x faster than CSV
Round-trip check: OK (5,000,000 rows preserved)
```

On 1,000,000 rows it was 3.7x. That's less than the 20x in the original blueprint — and I'm reporting the measured number, because Arrow's CSV reader is already fast, and honest benchmarks are what make a tool trustworthy. 6.6x on 5M rows, with zero code changes to the data itself, is still a real win, and the gap grows with row count and with slower, text-based parsers downstream.

## How it works

1. Producer serializes a table to Arrow IPC stream format
2. That stream is stored as a file in `/dev/shm` (shared memory), with a small `.json` metadata file: rows, columns, types, size, timestamp
3. Consumer opens it with `pyarrow.memory_map` and `ipc.open_stream`, so Arrow reads the table from shared memory instead of parsing text
4. `shmpipe top` lists live pipes, like `top` for data streams
5. `shmpipe cat` prints a pipe as CSV to stdout, so `grep`, `awk`, and `head` still work — that's the automatic fallback

## Polyglot story

- Python: `shmpipe.write_table()` / `read_table()` / `read_pandas()`, included and tested here
- R: `r/shmpipe.R` provides `shmpipe_read()` / `shmpipe_write()` using the R `arrow` package, reading the same `.arrow` file. **Honest note: this R code was not tested in this VM because R is not installed here.** It is included as the intended cross-language path, not as a verified result.
- C++ / Rust: any Arrow IPC reader can open the same file — that's the point of using a standard format, not a custom binary blob

## Requirements

- Python 3.9+, `pyarrow`
- Linux with `/dev/shm` for true shared memory; otherwise it falls back to a temp directory (still Arrow, just not RAM-shared)

Install in a venv:

```bash
python -m venv .venv && .venv/bin/pip install pyarrow
.venv/bin/python -m pytest tests/ -q
```

## Honest scope of this MVP

- No daemon, no ring buffer yet — a named file in shared memory is the simple, debuggable v1
- No live streaming of partial rows; a table is written, then read whole
- No schema evolution handling beyond what Arrow IPC already gives you
- The two-sided adoption problem from the earlier ranking still applies: both sides need to use ShmPipe (or Arrow) to get the speedup. `cat` is the bridge for classic tools.

## Layout

```
shmpipe/
  core.py  # Arrow IPC over /dev/shm, list/remove
  cli.py   # write / read / cat / top / rm
examples/benchmark.py
tests/test_shmpipe.py
r/shmpipe.R
```

## License

MIT
