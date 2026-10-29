# SecretScan — Check Before You Push

**Scan a file or folder for hardcoded secrets, before they reach GitHub.**

Once a secret is pushed, even if you delete it later, it can live in git history forever. SecretScan is a 30-second pre-push check: it flags AWS keys, GitHub tokens, Slack tokens, private key blocks, and generic `password = "..."` / `api_key = "..."` assignments, with the value redacted in output.

## Try it

```bash
python -m secretscan scan examples/leaky.py
# Found 3 potential secret(s) - check before pushing:
#   examples/leaky.py:3 [aws_access_key] AWS access key pattern -> AKIA***
#   examples/leaky.py:4 [github_token] GitHub personal access token pattern -> ghp_***
#   examples/leaky.py:5 [generic_password] Hardcoded password assignment -> pass***

python -m secretscan scan examples/clean.py
# No secrets found.
```

Exit code 1 = findings, 0 = clean. That makes it work in CI and as a pre-commit check.

## Fix a finding

1. Move the value to an environment variable (`os.environ.get(...)`)
2. If it was ever pushed, **rotate it** — deleting the line does not un-leak it
3. Add the file (especially `.env`) to `.gitignore`
4. To intentionally ignore a line (e.g. a documented example), add `# secretscan:ignore` to that line

## Limits (honest)

- Pattern matching, not proof: a flagged line might be a fake example key, and a real secret in an unusual format might be missed.
- It does not scan binary files, and it does not check git history — for history, use a dedicated tool like gitleaks / trufflehog.
- Values in output are redacted to first 4 + last 2 characters only.

## License

MIT, as part of GuardKit.
