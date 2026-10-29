"""SecretScan: scan files for hardcoded secrets before you push to GitHub.

Rule-based, no AI, no uploads. It looks for patterns, not for
"is this a real secret?" - a finding means "check this line before
you push", not "this is definitely a live key".

Patterns are deliberately for well-known formats plus generic
assignment patterns (password=..., api_key=... with a long value).
Test / example keys (AWS example key, etc.) are still flagged
in examples, so you can see the tool work - in real code, move
secrets to environment variables and add the file to .gitignore.
"""
import re
from pathlib import Path

PATTERNS = [
    ("aws_access_key", r"AKIA[0-9A-Z]{16}", "AWS access key pattern"),
    ("github_token", r"ghp_[A-Za-z0-9]{20,}", "GitHub personal access token pattern"),
    ("github_oauth", r"gho_[A-Za-z0-9]{20,}", "GitHub OAuth token pattern"),
    ("slack_token", r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token pattern"),
    ("private_key", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "Private key block"),
    ("generic_password", r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{8,}['\"]", "Hardcoded password assignment"),
    ("generic_api_key", r"(?i)(api[_-]?key|secret)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "Hardcoded API key / secret assignment"),
    ("aws_secret", r"(?i)aws_secret_access_key\s*=\s*['\"][A-Za-z0-9/+=]{20,}['\"]", "AWS secret access key assignment"),
    ("bearer_token", r"Bearer [A-Za-z0-9_\-\.]{20,}", "Bearer token in code"),
]

IGNORE_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
IGNORE_FILES = {".gitignore"}


def scan_text(text: str, path: str = "") -> list:
    findings = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if "secretscan:ignore" in line:
            continue
        for rule_id, pat, desc in PATTERNS:
            m = re.search(pat, line)
            if m:
                # Redact: for token-like values show first 4 + last 2 only;
                # for generic assignments show nothing, to avoid leaking the value.
                val = m.group(0)
                if rule_id.startswith("generic_") or rule_id == "aws_secret":
                    redacted = "***"
                else:
                    redacted = val[:4] + "***" + val[-2:] if len(val) > 8 else "***"
                findings.append({
                    "file": path, "line": lineno, "rule": rule_id,
                    "description": desc, "redacted": redacted,
                })
                break
    return findings


def check_env_gitignore(folder: Path) -> list:
    """Warn if a .env file exists but is not listed in .gitignore.

    This is the most common way secrets leak: the .env itself is
    scanned clean (it may contain real values, so we do NOT print
    them), but if it is not gitignored, the next commit will include it.
    Returns a list of warning strings (empty = ok or no .env file).
    """
    folder = Path(folder)
    env_files = [p for p in folder.rglob(".env*") if p.is_file() and ".git" not in p.parts]
    if not env_files:
        return []
    gitignore = folder / ".gitignore"
    ignored = gitignore.read_text(encoding="utf-8", errors="ignore") if gitignore.exists() else ""
    warnings = []
    for env in env_files:
        if ".env" not in ignored and env.name not in ignored:
            warnings.append(f"{env}: .env file exists but .gitignore does not list .env — add '.env' to .gitignore before committing.")
    return warnings


def scan_path(target: Path) -> list:
    findings = []
    if target.is_file():
        files = [target]
    else:
        files = []
        for p in sorted(target.rglob("*")):
            if not p.is_file():
                continue
            if any(part in IGNORE_DIRS for part in p.parts):
                continue
            if p.name in IGNORE_FILES:
                continue
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}:
                continue
            files.append(p)
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        findings.extend(scan_text(text, str(p)))
    return findings
