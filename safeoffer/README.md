# SafeOffer — Don't Pay Yet

**Paste a job, loan, or deal offer BEFORE you pay. Get a plain-language safety check in seconds.**

A fake job offer doesn't just cost money. In recent cases it has cost families 600,000–900,000 taka, left workers stranded abroad, and in the worst cases led to trafficking and scam compounds. There are long guides about this, but no instant, plain-language checker a family can use *before* the payment.

SafeOffer is that pause button.

## Try it in 30 seconds (no install, no account)

Open `index.html` in any browser — on a phone is fine. Checking happens in your browser. Nothing is uploaded, nothing is stored.

Click **"Load fake job example"** and press Check. Real output from this project:

```
Score: 100/100
Verdict: RED - DO NOT PAY YET  (লাল - এখনো টাকা দেবেন না)
Advice: Stop. Do not pay, do not hand over your passport, and verify with BMET / the embassy / the employer directly first.

Flags:
  - Job offered on a tourist / visit visa
  - Payment in cash with no receipt
  - Fee demanded before a visa or contract
  - Passport being kept / confiscated
  - Very large fee (6 lakh taka)
  - Destination caution: Cambodia
  - Urgency pressure, no experience / no interview, personal payment number
```

Click **"Load legit example"** and it correctly goes green (20/100, low risk on these checks only).

A loan scam example also goes red: 90/100.

## What it checks (explainable, not black-box AI)

- Tourist / visit visa for a job
- Cash payment, no receipt
- Fee before visa / offer letter / contract
- Passport kept / confiscated
- Very large fee (4–9 lakh range seen in fraud cases)
- Destination caution (e.g. Cambodia in recent reporting)
- Urgency, no experience / no interview, personal bKash number, contract signed after arrival

Score >= 60 = RED, 30–59 = AMBER, below 30 = GREEN (low risk on these checks only).

Every result comes with **5 questions to ask before paying**:

1. What is the recruiter's BMET licence number? Can I check it myself?
2. Will I get a work visa (not tourist) and a written contract BEFORE I pay?
3. Can I have an itemized fee breakdown and a receipt for every payment?
4. Can I contact the employer directly, without the agent in between?
5. What happens to my money if the visa is refused or the job does not exist?

All verdicts, advice, and questions are available in English and Bengali (বাংলা toggle).

## CLI version (same rules, for developers / CI)

```bash
python -m safeoffer check examples/fake_job_cambodia.txt
python -m safeoffer check examples/legit_example.txt
# exit code 1 = RED, 0 = otherwise
```

## Privacy and limits — please read

- **Never paste your passport, bank details, or personal ID.** Paste the offer, not your identity.
- This is **not legal advice** and does **not prove** an offer is legitimate. A green result only means no major flags were found in that text.
- Always verify officially: BMET licence list, the embassy, and the employer directly, by a contact you find yourself — not one the agent gives you.
- Forged documents cannot be perfectly detected by text alone. SafeOffer is a safety pause, not a guarantee.

## Why this is different from CheckFirst

CheckFirst (held, separate idea) asks: *is this message true?*
SafeOffer asks: *is it safe to pay and travel?*

Different decision, different data (licences, visa type, fees, destination), different stakes.

## Open pattern library

The rules in `safeoffer/checker.py` and `app.js` are the open pattern library. Anyone can add a new scam pattern with a plain-language reason, in English and Bengali, and the whole community benefits — like a Wikipedia for offer safety, not a closed company database.

## Layout

```
index.html, app.js, style.css   # web app, client-side only
safeoffer/
  checker.py  # rules, scoring, Bengali + English reasons
  cli.py      # python -m safeoffer check
examples/
  fake_job_cambodia.txt, loan_scam.txt, legit_example.txt
tests/test_checker.py
```

## License

MIT
