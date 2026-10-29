from pathlib import Path
from secretscan import scan_path, scan_text

BASE = Path(__file__).parent.parent / "examples"


def test_leaky_is_flagged():
    findings = scan_path(BASE / "leaky.py")
    assert len(findings) >= 2
    rules = {f["rule"] for f in findings}
    assert "aws_access_key" in rules
    assert "github_token" in rules


def test_clean_is_not_flagged():
    assert scan_path(BASE / "clean.py") == []


def test_ignore_comment():
    text = 'password = "supersecretpassword123"  # secretscan:ignore\n'
    assert scan_text(text) == []
