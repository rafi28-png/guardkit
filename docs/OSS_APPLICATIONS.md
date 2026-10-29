# GuardKit for Claude for OSS + Codex for OSS — honest application plan

**Do not submit this with inflated numbers. Both programs say misleading metrics can cause rejection or revocation. Submit only what is true on the day you submit, and update it as GuardKit grows.**

## What the two offers actually are

### Claude for Open Source (Anthropic)
- 6 months of free Claude Max 20x, via claude.com/contact-sales/claude-for-oss
- Official "Who should apply" tracks (any ONE track is enough to apply):
  1. **Maintainers / library authors:** 500+ dependent repos, OR 100+ dependent packages, OR 200,000+ combined monthly downloads (npm, PyPI, crates.io, RubyGems, etc.)
  2. **Core contributors:** listed committer/maintainer on a recognized foundation/language project (CPython, Rust team, Node.js TSC, Apache PMC, CNCF, Kubernetes, Linux kernel, Django, Rails, or similar)
  3. **Active contributors:** 100+ pull requests merged into repos you don't own in the last 12 months
  4. **Community builders:** one repo with 20+ unique external contributors with merged PRs in the last 12 months
  5. **Critical infrastructure:** a repo you maintain with an OpenSSF criticality score of 0.4 or above
- Plus, in Anthropic's own words: "Don't quite fit? If you maintain something the ecosystem quietly depends on, apply anyway and tell us about it."
- After 6 months, the complimentary subscription ends; a prior paid plan resumes unless cancelled, otherwise the account returns to free.

### Codex for Open Source (OpenAI)
- Via openai.com/form/codex-for-oss/
- For maintainers behind critical open-source software — people who review PRs, triage issues, maintain releases, and preserve security/code quality.
- Selected maintainers receive: 6 months of ChatGPT Pro (including Codex), conditional access to Codex Security, and API credits for coding, maintainer automation, release workflows, and core open-source work.
- **No numeric star/download threshold is published on the official Codex page itself.** Third-party reports conflict (some say 1,000 stars, some say 5,000, some say no minimum). Do not quote a threshold as official. What OpenAI does ask for, in its form and terms as reported: primary/core maintainer status, public repo URL, ecosystem importance, active maintenance (PR review, issue triage, releases), and how you would use API credits. Selection is discretionary, rolling, and not guaranteed.

## GuardKit today — honest checklist (2026-10-30)

| Criterion | GuardKit today | Status |
|---|---|---|
| Public GitHub repo | **Not published yet** — all work is local in `guardkit/` | ❌ NOT YET — Step 1 |
| OSI-approved license | MIT, in every tool folder + top level | ✅ Yes |
| Active maintenance (recent commits/releases) | No public history yet — 1 day of local work, v0.6.4, changelog exists | ❌ NOT YET publicly |
| Stars / dependents / downloads | 0 / 0 / 0 (not published, not on PyPI) | ❌ Not meeting Claude Track 1 |
| External contributors | 0 | ❌ Not meeting Claude Track 4 |
| OpenSSF criticality ≥0.4 | No score — score requires public repo + usage | ❌ Not yet |
| 100+ merged PRs to other repos (12 mo) | Not established for Tiara | ❌ Not a current track |
| Core contributor to CPython/Rust/etc. | No | ❌ Not a current track |
| Real, working code + tests + demo proof | 7 tools, 16 pytest tests, demo ALL PASS, selfcheck CLEAN, web app | ✅ Yes — this is the foundation |
| Worldwide, English primary | Yes, Bengali supported, not Bengali-only | ✅ Yes |

**Verdict today: GuardKit does NOT meet Claude's published numeric tracks, and is weak for Codex on adoption/maintenance history alone. It is not ready to submit as a "qualifying" project today. It IS ready to publish and start the clock.**

## The realistic path (in order)

### Step 1 — Publish (this week, no coding needed)
Follow `UPLOAD_TO_GITHUB.md`. Publish `guardkit/` as a public repo, turn on GitHub Pages for `web/landing.html` + `web/index.html`. This starts your public maintenance history. Without this, neither application can be verified.

### Step 2 — Make ONE tool actually installable and used (next 2–4 weeks)
Do not try to grow all 7 at once. Reviewers look for *one* project people depend on.

**Best candidate: SemVer-Diff** — the only tool in the suite that other developers would pip-install and put in CI. It solves a real, repeated pain (silent breaking changes in a "safe" patch) for every Python library author.
**Second candidate: SecretScan** — useful as a pre-commit / CI check, easy to adopt.

For SemVer-Diff:
- Publish to PyPI as `semver-diff` (check name availability first — if taken, use `semver-diff-check` or similar, and update pyproject + README together).
- Add it to GitHub Actions in GuardKit itself (dogfooding: GuardKit's own CI should run SemVer-Diff on itself).
- Write one clear example: "I ran this on library X, it found Y" — real, not invented.
- Release v0.1.0, then v0.1.1, v0.2.0 with a changelog. Releases are maintenance evidence.

### Step 3 — Build the signals reviewers actually check (next 1–6 months)
- **Issues + triage:** keep issues open, answer them, label `good first issue` for small pattern additions (CheckFirst/SafeOffer patterns are perfect first issues — no deep code needed).
- **External contributors:** invite pattern contributions via the scam-pattern issue template already in `.github/ISSUE_TEMPLATE/`. 20 external contributors is Claude Track 4 — it will not happen in a week, but it is the most achievable Claude track for a trust tool, because adding a scam pattern is a 5-line PR.
- **Downloads / dependents:** PyPI downloads for SemVer-Diff / SecretScan, plus GitHub dependents (repos that use GuardKit in CI). Document them honestly when they exist.
- **OpenSSF score:** once the repo is public and used, check its OpenSSF criticality score. Do not claim 0.4 until you have measured it.

### Step 4 — Apply, in this order, with honest text

**Apply to Codex first.** It has no published numeric bar, it explicitly values ecosystem importance + active maintenance, and its form asks for a short qualification story. Use the draft below, updated with your real repo URL and real numbers on the day you apply.

**Apply to Claude via the "apply anyway" track** only after Step 1–3 have produced *something* real to point to (public repo, at least one PyPI release, at least a few external users/issues). If you apply today with 0 stars / 0 downloads, you will almost certainly be rejected on the numeric tracks, and a rejection with inflated claims would hurt a later honest application.

## Draft application texts — honest, under 500 characters each (update numbers before submitting)

### Codex — qualification (copy, then replace [brackets])
> Primary maintainer of GuardKit, a worldwide open-source suite (MIT) of 7 Python tools for trust and pipelines: SemVer-Diff (behavioral breaking-change detection), CheckFirst/SafeOffer (scam and offer safety, English + Bengali support), SecretScan, TraceLock, WattShift, ShmPipe. Public repo: [URL]. I triage issues, review pattern PRs, maintain releases and CI, and use it in my own workflows. I would use Codex for issue triage, PR review, and release automation.

### Codex — API credits use
> Automate issue triage for new scam patterns, review contributor PRs for CheckFirst/SafeOffer rules, run release notes and changelog generation, and audit SecretScan patterns for false positives — all maintainer work, not bulk code generation.

### Claude — "apply anyway" explanation
> I maintain GuardKit, a MIT-licensed suite of 7 tools that the Python ecosystem quietly needs: a behavioral SemVer checker, a secret scanner, and scam/offer safety checkers used by ordinary phone users worldwide. It is early and does not yet meet the 500-dependent / 200k-download bar, but it is actively maintained, tested (demo + pytest), and designed to be depended on in CI. I am applying on ecosystem importance, not on inflated metrics.

## What NOT to do

- Do not buy, exchange, or farm stars, downloads, or contributors. Both programs forbid misleading metrics and can revoke benefits.
- Do not claim PyPI downloads, dependents, or an OpenSSF score you have not measured.
- Do not submit a repo that is not public, or a repo you do not actually maintain.
- Do not apply to both programs with different stories — use the same honest repo URL and role in both.

## Sources (official pages, checked 2026-10-30)

- Claude for Open Source: https://claude.com/contact-sales/claude-for-oss
- Codex for Open Source: https://openai.com/form/codex-for-oss/
