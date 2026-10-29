from pathlib import Path
from checkfirst import check

BASE = Path(__file__).parent.parent / "examples"


def test_scam_is_red():
    r = check((BASE / "scam_forward.txt").read_text())
    assert r["score"] >= 60
    assert r["verdict"].startswith("RED")
    ids = {f["id"] for f in r["flags"]}
    assert "otp_request" in ids
    assert "lottery_prize" in ids


def test_health_rumor_is_red():
    r = check((BASE / "health_rumor.txt").read_text())
    assert r["score"] >= 60
    ids = {f["id"] for f in r["flags"]}
    assert "health_cure" in ids


def test_legit_is_not_red():
    r = check((BASE / "legit_example.txt").read_text())
    assert r["score"] < 60
