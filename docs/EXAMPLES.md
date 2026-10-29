# GuardKit Examples — expected results

Every example below is in the repo, and its score was actually run. Use these to try GuardKit in 30 seconds, without writing your own test case.

## CheckFirst — messages

| File | Expected | Why |
|---|---|---|
| `checkfirst/examples/scam_forward.txt` | 100/100 RED | OTP, lottery, fee, chain forward, urgency, bit.ly, bKash impersonation |
| `checkfirst/examples/bangla_scam.txt` | 100/100 RED | Same patterns in Bengali |
| `checkfirst/examples/health_rumor.txt` | 70/100 RED | "Cures cancer in 3 days, 100% guaranteed, forward to 10 people" |
| `checkfirst/examples/legit_example.txt` | 0/100 GREEN | Official Bangladesh Bank notice, bb.org.bd, dated |
| `checkfirst/examples/bangla_legit.txt` | 0/100 GREEN | Same official notice in Bengali — proves Bengali legit is not flagged |

## SafeOffer — offers

| File | Expected | Why |
|---|---|---|
| `safeoffer/examples/fake_job_cambodia.txt` | 100/100 RED | Tourist visa, cash no receipt, 6 lakh fee, passport kept, Cambodia, urgency |
| `safeoffer/examples/bangla_fake_job.txt` | 100/100 RED | Same patterns in Bengali |
| `safeoffer/examples/loan_scam.txt` | 90/100 RED | Loan scam patterns |
| `safeoffer/examples/legit_example.txt` | 20/100 GREEN | BMET, work visa, interview, contract before payment, itemized receipt |
| `safeoffer/examples/worldwide_legit.txt` | 20/100 GREEN | Same legit pattern, worldwide wording (no country-specific regulator name) |

## Other tools

| Tool | Example | Expected |
|---|---|---|
| SemVer-Diff | `semver-diff/examples/old/math_utils.py` vs `new/` | 4 divergences, BEHAVIOR CHANGE DETECTED |
| TraceLock | `tracelock/examples/pipeline.py` | No alerts; corrupt version alerts on 50% empty cells |
| WattShift | `wattshift/examples/forecast.json` | Saved 350g CO2 (60.3%) for 2 kWh |
| ShmPipe | `shmpipe/examples/benchmark.py 1000000` | Round-trip OK, faster than CSV |
| SecretScan | `secretscan/examples/leaky.py` / `clean.py` | Leaky: 3 findings, exit 1. Clean: 0, exit 0 |

## Try them all at once

```bash
python kit.py demo
python kit.py check checkfirst/examples/bangla_scam.txt
python kit.py check safeoffer/examples/worldwide_legit.txt
```
