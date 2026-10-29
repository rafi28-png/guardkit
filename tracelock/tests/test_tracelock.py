import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def run_demo(tmp_path, script):
    demo = tmp_path / "demo"
    demo.mkdir()
    shutil.copy(ROOT / "examples" / "pipeline.py", demo / "pipeline.py")
    shutil.copy(ROOT / "examples" / "corrupt_pipeline.py", demo / "corrupt_pipeline.py")
    shutil.copy(ROOT / "examples" / "raw.csv", demo / "raw.csv")
    result = subprocess.run(
        [sys.executable, "-m", "tracelock", "run", "--workdir", str(demo),
         "--out", str(tmp_path / "prov.json"), "--report", str(tmp_path / "report.md"),
         "--", sys.executable, *script.split()],
        cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads((tmp_path / "prov.json").read_text())


def test_good_pipeline_has_no_alerts(tmp_path):
    prov = run_demo(tmp_path, "pipeline.py raw.csv cleaned.csv")
    assert "raw.csv" in [e["path"] for e in prov["inputs"]]
    assert "cleaned.csv" in [e["path"] for e in prov["outputs"]]
    assert prov["alerts"] == []


def test_corrupt_pipeline_alerts(tmp_path):
    prov = run_demo(tmp_path, "corrupt_pipeline.py cleaned.csv")
    assert prov["alerts"], "corrupt output should trigger an alert"
