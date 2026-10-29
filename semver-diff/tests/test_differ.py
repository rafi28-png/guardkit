from semver_diff.differ import compare_files
import pathlib

BASE = pathlib.Path(__file__).parent.parent / "examples"


def test_detects_silent_breaking_change():
    report = compare_files(str(BASE / "old" / "math_utils.py"),
                           str(BASE / "new" / "math_utils.py"))
    assert report.divergences
    funcs = {d.function for d in report.divergences}
    assert "round_half" in funcs
    assert "handle_missing" in funcs


def test_same_version_has_no_divergences():
    report = compare_files(str(BASE / "old" / "math_utils.py"),
                           str(BASE / "old" / "math_utils.py"))
    assert report.divergences == []
    assert "PATCH looks safe" in report.verdict
