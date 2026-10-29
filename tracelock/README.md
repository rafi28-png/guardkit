# TraceLock

**Run your existing pipeline unchanged, and get proof of exactly what went in and what came out.**

Six months later, nobody can prove which dataset version, script, or flags produced a plot or model. Workflow managers fix this by making you rewrite everything. TraceLock doesn't: you just wrap your existing command.

```bash
python -m tracelock run -- python3 pipeline.py raw.csv cleaned.csv
```

No code changes to your scripts. No new DSL.

## What it does

1. **Watches I/O at OS level (Linux):** Uses `strace -f` to see every file your command and its subprocesses open, filtered to your project folder. On systems without strace, it falls back to a before/after snapshot diff.
2. **Hashes inputs and outputs:** SHA-256 (short form) for every input and output file, so a later change is detectable.
3. **Checks tabular health on the fly:** For CSV outputs it counts rows, columns, and empty cells, and alerts immediately if an output is empty, is 50%+ empty, or drops to less than half the input row count.
4. **Writes a provenance label:** `provenance.lock.json` with command, exit code, duration, Python/platform, input/output hashes and stats, and alerts.
5. **Draws the lineage:** `report.md` contains a Mermaid flowchart: inputs → command → outputs.

## Real demo output

Good pipeline:

```
Wrote 5 rows to cleaned.csv
Exit code: 0
Inputs: ['pipeline.py', 'raw.csv']
Outputs: ['cleaned.csv']
Alerts: none
```

Corrupt pipeline (same command shape, but it writes empty values):

```
Wrote corrupted output
Exit code: 0
Inputs: ['corrupt_pipeline.py']
Outputs: ['cleaned.csv']
Alerts:
  - cleaned.csv: 50% empty cells - possible silent corruption
```

That second case is the point: the corrupt script *succeeds* (exit 0) and would silently poison downstream steps without TraceLock.

## Try it

```bash
# in a demo folder with pipeline.py + raw.csv
python -m tracelock run --workdir demo -- python3 pipeline.py raw.csv cleaned.csv
cat provenance.lock.json
cat report.md
```

## Honest scope of this MVP

- Linux + strace for full tracing; snapshot fallback elsewhere
- CSV stats only for now (Parquet/Arrow is v2)
- Hashing is SHA-256 in this MVP; BLAKE3 is a drop-in speed upgrade
- It proves *what files* went in/out and their health, not full eBPF-level syscall provenance yet

## Layout

```
tracelock/
  hashing.py  # snapshots + hashes
  tracer.py   # strace parsing + fallback
  stats.py    # CSV row / missingness stats
  report.py   # provenance.lock.json + Mermaid report
  cli.py      # tracelock run --
examples/
  pipeline.py, raw.csv, corrupt_pipeline.py
tests/
  test_tracelock.py
```

## License

MIT
