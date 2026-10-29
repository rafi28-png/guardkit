"""CLI: shmpipe write <name> <csv> | read <name> <out.csv> | cat <name> | top | rm <name>"""
import argparse
import sys


def main(argv=None) -> int:
    from . import core

    parser = argparse.ArgumentParser(prog="shmpipe")
    sub = parser.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("write", help="Load a CSV into shared memory")
    w.add_argument("name")
    w.add_argument("csv_path")

    r = sub.add_parser("read", help="Read a pipe back out to CSV")
    r.add_argument("name")
    r.add_argument("out_csv")

    c = sub.add_parser("cat", help="Print a pipe as CSV to stdout (classic Unix fallback: pipe this to grep/head)")
    c.add_argument("name")

    sub.add_parser("top", help="Show live pipes, like `top` for data streams")
    rm = sub.add_parser("rm", help="Delete a pipe")
    rm.add_argument("name")

    args = parser.parse_args(argv)

    if args.cmd == "write":
        import pyarrow.csv as pa_csv
        table = pa_csv.read_csv(args.csv_path)
        meta = core.write_table(args.name, table)
        print(f"Wrote {meta['rows']} rows, {meta['size_bytes']} bytes to shared memory as {args.name!r}")
        return 0
    if args.cmd == "read":
        import pyarrow.csv as pa_csv
        table = core.read_table(args.name)
        with open(args.out_csv, "wb") as f:
            pa_csv.write_csv(table, f)
        print(f"Wrote {table.num_rows} rows to {args.out_csv}")
        return 0
    if args.cmd == "cat":
        import io
        import pyarrow.csv as pa_csv
        table = core.read_table(args.name)
        # Text fallback for grep/awk/head, using Arrow's own CSV writer (no pandas needed)
        sink = io.BytesIO()
        pa_csv.write_csv(table, sink)
        sys.stdout.write(sink.getvalue().decode("utf-8"))
        return 0
    if args.cmd == "top":
        pipes = core.list_pipes()
        if not pipes:
            print("No active ShmPipes.")
            return 0
        print(f"{'NAME':<20} {'ROWS':>10} {'SIZE':>12}  COLUMNS")
        for p in pipes:
            cols = ",".join(c["name"] for c in p["columns"])
            print(f"{p['name']:<20} {p['rows']:>10} {p['size_bytes']:>12}  {cols}")
        return 0
    if args.cmd == "rm":
        print("Removed." if core.remove(args.name) else "Not found.")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
