"""Suite smoke tests: each tool's core checker must give its expected verdict (now 7 tools)."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _add(folder, pkg):
    p = ROOT / folder
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def test_all_seven():
    _add("semver-diff", "semver_diff")
    from semver_diff.differ import compare_files
    r = compare_files(str(ROOT / "semver-diff" / "examples" / "old" / "math_utils.py"),
                      str(ROOT / "semver-diff" / "examples" / "new" / "math_utils.py"))
    assert len(r.divergences) == 4

    _add("safeoffer", "safeoffer")
    from safeoffer import check as safe_check
    assert safe_check((ROOT / "safeoffer" / "examples" / "fake_job_cambodia.txt").read_text())["score"] >= 60

    _add("checkfirst", "checkfirst")
    from checkfirst import check as cf_check
    assert cf_check((ROOT / "checkfirst" / "examples" / "scam_forward.txt").read_text())["score"] >= 60

    _add("wattshift", "wattshift")
    from wattshift.optimizer import find_best_window, carbon_math
    import json
    f = json.loads((ROOT / "wattshift" / "examples" / "forecast.json").read_text())
    v = find_best_window(f, 60, 4, "2026-10-30T00:00:00+00:00")
    assert v["best_start"] == "2026-10-30T01:00:00+00:00"
    assert carbon_math(v, 2.0)["saved_co2_g"] == 350.0

    _add("secretscan", "secretscan")
    from secretscan import scan_path, check_env_gitignore
    assert len(scan_path(ROOT / "secretscan" / "examples" / "leaky.py")) >= 2
    assert scan_path(ROOT / "secretscan" / "examples" / "clean.py") == []
    # New patterns added in v0.4.0 / v0.5.0 must actually fire
    assert any(f["id"] == "punycode_link" for f in cf_check("Click xn--bkash-abc.com to win")["flags"])
    assert any(f["id"] == "extra_fee_before_contract" for f in safe_check("Job, work permit fee 50000 taka before contract")["flags"])
    # Bengali examples must both be RED
    assert cf_check((ROOT / "checkfirst" / "examples" / "bangla_scam.txt").read_text())["score"] == 100
    assert safe_check((ROOT / "safeoffer" / "examples" / "bangla_fake_job.txt").read_text())["score"] == 100
    # Legit examples must NOT be RED — including the new Bengali legit and worldwide legit
    assert cf_check((ROOT / "checkfirst" / "examples" / "bangla_legit.txt").read_text())["score"] == 0
    assert safe_check((ROOT / "safeoffer" / "examples" / "worldwide_legit.txt").read_text())["score"] < 30
    # .env gitignore warning: warns without gitignore, silent with it
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / ".env").write_text("KEY=abc")
        assert check_env_gitignore(td), "should warn when .env is not gitignored"
        (td / ".gitignore").write_text(".env\n")
        assert check_env_gitignore(td) == []
    # Backward-compatible alias (old name, seven tools now)
    # (defined below, after test_all_seven)

    # kit.py check / selfcheck logic: missing file and empty file must NOT give a misleading GREEN
    import subprocess
    r = subprocess.run([sys.executable, "kit.py", "check", "/nonexistent-guardkit-test.txt"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 2 and "not found" in r.stdout.lower()
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as tf:
        tf.write("")
        empty_path = tf.name
    r = subprocess.run([sys.executable, "kit.py", "check", empty_path], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 2 and "empty" in r.stdout.lower()

    # TraceLock and ShmPipe are covered by demo_all.py (TraceLock needs a temp workdir,
    # ShmPipe needs pyarrow) - their own folders have their own tests.
    assert (ROOT / "tracelock" / "tracelock" / "cli.py").exists()
    assert (ROOT / "shmpipe" / "shmpipe" / "core.py").exists()
    assert (ROOT / "web" / "index.html").exists()
    assert (ROOT / "kit.py").exists()

# Backward-compatible alias: old name test_all_six, now seven tools.
test_all_six = test_all_seven
