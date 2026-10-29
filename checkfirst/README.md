# CheckFirst — Check Before You Forward

**Paste a forwarded message BEFORE you forward it. Get a plain-language check in seconds.**

Misinformation doesn't spread as articles. It spreads as forwarded messages, often in Bengali, from a trusted contact — a lottery win, an OTP request, a health cure, an old photo shared as if new. Journalist fact-checkers are slow, English, and built for articles. CheckFirst is built for that moment, for ordinary phone users, in English and Bengali.

## Try it in 30 seconds (no install, no account)

Open `index.html` in any browser — on a phone is fine. Checking happens in your browser. Nothing is uploaded, nothing is stored.

Click **"Load scam example"**:

```
Score: 100/100
Verdict: RED - LIKELY SCAM / MISINFORMATION - DO NOT FORWARD
Flags: OTP request, lottery prize, fee to claim, chain forward,
urgency, shortened link, bKash impersonation
What to do: Do NOT send OTP or money, do NOT click, do NOT forward, report it.
```

Click **"Load health rumor example"**: 70/100, RED — cure for cancer in 3 days, 100% guaranteed, chain forward, no source.

Click **"Load legit example"**: 0/100, GREEN — no major flags found (still not proof it is true).

## What it checks (explainable, not black-box AI)

- OTP request — real banks / bKash NEVER ask for your OTP
- Lottery / prize you never entered
- Fee to claim a prize / loan / offer
- Health cure claims for serious diseases, in days, with 100% guarantee
- Vague "scientists say" with no study, journal, or link
- Chain messages asking you to forward to many people
- Urgency / threats ("account will be blocked today")
- Shortened links hiding the real destination
- Impersonation (bKash / bank / government) + click / pay request

Score >= 60 = RED, 30–59 = AMBER, below 30 = GREEN.

Every result gives you a **shareable summary** — copy that, not the original message — so you can warn others without spreading the scam.

## How it is different from SafeOffer

SafeOffer (separate project) asks: *is it safe to pay and travel for a job / loan?*
CheckFirst asks: *is this forwarded message safe to forward, click, or believe?*

Different decision, different checks, same plain-language, worldwide philosophy — English primary, Bengali supported.

## Privacy and limits — please read

- **Never paste OTP, passwords, or bank details.** Paste the message, not your identity.
- This **flags patterns, it does NOT prove truth or falsehood**. A green result only means no major flags were found in that text.
- Always verify with an official / reputable source you find yourself, not a link in the message.
- For health claims, ask a doctor — do not change treatment based on a forward.
- For images: this MVP checks text and links. A photo check (reverse search, date, reuse) is v2 — for now, the app tells you to check the date and source before forwarding a photo.

## CLI version (same rules)

```bash
python -m checkfirst check examples/scam_forward.txt
python -m checkfirst check examples/health_rumor.txt
python -m checkfirst check examples/legit_example.txt
# exit code 1 = RED, 0 = otherwise
```

## Open pattern library

Rules live in `checkfirst/checker.py` and `app.js`, in English and Bengali, with a plain-language reason for each. Anyone can add a new pattern — like a Wikipedia for message safety, not a closed company database.

## Layout

```
index.html, app.js, style.css   # web app, client-side only
checkfirst/
  checker.py  # rules, scoring, Bengali + English reasons
  cli.py      # python -m checkfirst check
examples/
  scam_forward.txt, health_rumor.txt, legit_example.txt
tests/test_checker.py
```

## License

MIT
