from pathlib import Path
from safeoffer import check

BASE = Path(__file__).parent.parent / "examples"


def test_fake_job_is_red():
    result = check((BASE / "fake_job_cambodia.txt").read_text())
    assert result["score"] >= 60
    assert result["verdict"].startswith("RED")
    ids = {f["id"] for f in result["flags"]}
    assert "tourist_visa_job" in ids
    assert "cash_no_receipt" in ids
    assert "passport_kept" in ids


def test_loan_scam_is_red_or_amber():
    result = check((BASE / "loan_scam.txt").read_text())
    assert result["score"] >= 30
    ids = {f["id"] for f in result["flags"]}
    assert "pay_before_visa" in ids or "personal_payment" in ids


def test_legit_example_is_not_red():
    result = check((BASE / "legit_example.txt").read_text())
    assert result["score"] < 60
    assert result["positives"], "legit example should show positive signs"
