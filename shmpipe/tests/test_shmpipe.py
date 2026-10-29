import pyarrow as pa
from shmpipe import read_table, write_table, list_pipes, remove


def test_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("SHMPIPE_DIR", str(tmp_path))
    table = pa.table({"id": [1, 2, 3], "value": [1.5, 2.5, 3.5]})
    write_table("demo", table)
    back = read_table("demo")
    assert back.num_rows == 3
    assert back.column("id").to_pylist() == [1, 2, 3]
    assert any(p["name"] == "demo" for p in list_pipes())
    assert remove("demo") is True
