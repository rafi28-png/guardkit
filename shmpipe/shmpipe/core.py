"""Core: Apache Arrow IPC over a memory-mapped file in shared memory.

The file lives in /dev/shm (RAM, on Linux) so a second process can
open it with pyarrow's memory_map and read the Arrow table without
copying it through CSV text or a disk file first.

If pyarrow is not installed, this module raises a clear error
telling the user to install it, instead of silently falling back
to a slower format.
"""
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def get_shm_dir() -> Path:
    override = os.environ.get("SHMPIPE_DIR")
    if override:
        p = Path(override)
        p.mkdir(parents=True, exist_ok=True)
        return p
    dev_shm = Path("/dev/shm")
    if dev_shm.is_dir() and os.access(dev_shm, os.W_OK):
        return dev_shm
    import tempfile
    p = Path(tempfile.gettempdir()) / "shmpipe"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _check_name(name: str):
    if not _NAME_RE.match(name):
        raise ValueError(f"Invalid pipe name {name!r}: use letters, numbers, - and _ only")


def _paths(name: str):
    _check_name(name)
    d = get_shm_dir()
    return d / f"shmpipe-{name}.arrow", d / f"shmpipe-{name}.json"


def _pa():
    try:
        import pyarrow as pa
        return pa
    except ImportError as exc:
        raise ImportError(
            "ShmPipe needs pyarrow: pip install pyarrow  (or use the venv in the README)"
        ) from exc


def write_table(name: str, table) -> dict:
    """Write a pyarrow Table (or pandas DataFrame) to shared memory."""
    pa = _pa()
    # Accept pandas DataFrames for convenience
    if table.__class__.__name__ == "DataFrame":
        table = pa.Table.from_pandas(table)
    data_path, meta_path = _paths(name)
    # Serialize to Arrow IPC stream bytes, then write to the shm file.
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)
    buf = sink.getvalue().to_pybytes()
    data_path.write_bytes(buf)
    meta = {
        "name": name,
        "format": "arrow-ipc",
        "rows": table.num_rows,
        "columns": [{"name": f.name, "type": str(f.type)} for f in table.schema],
        "size_bytes": len(buf),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "shm_dir": str(get_shm_dir()),
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def read_table(name: str):
    """Read a table via memory_map - no CSV parsing, no disk copy."""
    pa = _pa()
    data_path, _meta_path = _paths(name)
    if not data_path.exists():
        raise FileNotFoundError(f"No ShmPipe named {name!r} in {get_shm_dir()}")
    # memory_map gives Arrow a view of the file in shared memory.
    source = pa.memory_map(str(data_path), "r")
    with pa.ipc.open_stream(source) as reader:
        return reader.read_all()


def read_pandas(name: str):
    return read_table(name).to_pandas()


def list_pipes() -> list:
    out = []
    for meta_path in sorted(get_shm_dir().glob("shmpipe-*.json")):
        try:
            out.append(json.loads(meta_path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return out


def remove(name: str) -> bool:
    data_path, meta_path = _paths(name)
    found = False
    for p in (data_path, meta_path):
        if p.exists():
            p.unlink()
            found = True
    return found
