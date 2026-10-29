"""SafeOffer checker: explainable, rule-based, no AI, no uploads.

Each rule is a pattern + a plain-language reason + a weight.
Score >= 60 = RED / Do not pay yet. 30-59 = AMBER / Verify first.
Below 30 = GREEN / Low risk on these checks only - still verify officially.

This is NOT legal advice and does NOT prove an offer is legitimate.
It is a safety pause button before a payment or travel decision.
Always verify with BMET, the embassy, and the employer directly.
"""
import re

# (id, level, weight, patterns, reason_en, reason_bn)
RULES = [
    ("tourist_visa_job", "red", 30,
     [r"tourist visa", r"visit visa", r"tourist.*job", r"ট্যুরিস্ট ভিসা", r"ভিজিট ভিসা"],
     "Job offered on a tourist / visit visa - you could arrive jobless and undocumented.",
     "ট্যুরিস্ট / ভিজিট ভিসায় চাকরি - পৌঁছে চাকরি নাও থাকতে পারে।"),
    ("cash_no_receipt", "red", 25,
     [r"cash", r"no receipt", r"without receipt", r"নগদ", r"রসিদ ছাড়া"],
     "Payment in cash with no receipt is almost impossible to trace or recover.",
     "রসিদ ছাড়া নগদ টাকা ফেরত পাওয়া প্রায় অসম্ভব।"),
    ("pay_before_visa", "red", 25,
     [r"pay before", r"pay.*before.*visa", r"advance.*fee", r"processing fee", r"আগে টাকা", r"অগ্রিম"],
     "Fee demanded before a visa, offer letter, or contract is issued.",
     "ভিসা / অফার লেটার পাওয়ার আগেই টাকা চাওয়া হচ্ছে।"),
    ("passport_kept", "red", 30,
     [r"passport.*kept", r"passport.*confiscat", r"passport will be", r"পাসপোর্ট.*রাখ", r"পাসপোর্ট.*জমা"],
     "Passport being kept / confiscated is a classic trafficking red flag.",
     "পাসপোর্ট রেখে দেওয়া মানব পাচারের বড় লক্ষণ।"),
    ("high_fee", "red", 20,
     [r"6 lakh", r"600,?000", r"900,?000", r"5 lakh", r"4 lakh", r"৬ লাখ", r"৫ লাখ"],
     "Very large fee mentioned (4-9 lakh taka range seen in recent fraud cases). Compare with the official fee and get an itemized breakdown.",
     "খুব বড় অঙ্কের ফি - সরকারি ফির সঙ্গে মিলিয়ে দেখুন এবং বিস্তারিত হিসাব চান।"),
    ("destination_caution", "red", 20,
     [r"cambodia", r"কম্বোডিয়া"],
     "Destination caution: Cambodia has been reported as a route for scam compounds and was described as not a legitimate destination for Bangladeshi workers in recent reporting. Verify extra carefully.",
     "সতর্কতা: কম্বোডিয়া সম্পর্কে সাম্প্রতিক প্রতিবেদনে স্ক্যাম সেন্টারের কথা বলা হয়েছে। বাড়তি যাচাই করুন।"),
    ("urgency", "amber", 15,
     [r"urgent", r"today only", r"last seat", r"quick departure", r"limited offer", r"জরুরি", r"আজই", r"শেষ সুযোগ"],
     "Urgency pressure ('today only', 'last seat') is a common scam tactic to stop you checking.",
     "তাড়াহুড়ো করানো ('আজই', 'শেষ সুযোগ') স্ক্যামের সাধারণ কৌশল।"),
    ("no_experience_no_interview", "amber", 15,
     [r"no experience", r"no interview", r"no experience required", r"অভিজ্ঞতা লাগবে না", r"ইন্টারভিউ ছাড়া"],
     "High salary with no experience and no interview - verify the employer really exists.",
     "অভিজ্ঞতা / ইন্টারভিউ ছাড়া বেশি বেতন - নিয়োগকর্তা সত্যিই আছে কিনা যাচাই করুন।"),
    ("personal_payment", "amber", 15,
     [r"bkash.*personal", r"personal.*bkash", r"personal number", r"send.*bkash", r"বিকাশ.*পার্সোনাল", r"ব্যক্তিগত.*বিকাশ"],
     "Payment to a personal bKash / personal number, not a company bank account.",
     "কোম্পানির ব্যাংক অ্যাকাউন্ট নয়, ব্যক্তিগত বিকাশ / নম্বরে টাকা পাঠাতে বলা হচ্ছে।"),
    ("contract_later", "amber", 15,
     [r"sign.*abroad", r"sign.*after.*arriv", r"contract.*later", r"পরে.*চুক্তি", r"বিদেশে.*সই"],
     "Contract to be signed after arrival - risk of contract substitution with lower pay.",
     "পৌঁছানোর পর চুক্তি সই - বেতন কমিয়ে দেওয়ার ঝুঁকি থাকে।"),
    ("extra_fee_before_contract", "amber", 25,
     [r"work permit.*fee", r"medical.*fee", r"training.*fee", r"ওয়ার্ক পারমিট.*ফি", r"মেডিকেল.*ফি"],
     "Extra fee for work permit / medical / training demanded before a contract. Ask why, get it in writing, and compare with official fees.",
     "চুক্তির আগে ওয়ার্ক পারমিট / মেডিকেল / ট্রেনিং ফি চাওয়া হচ্ছে - লিখিত হিসাব চান।"),
    ("fee_mentioned", "amber", 10,
     [r"fee", r"ফি", r"টাকা দিতে"],
     "A fee is mentioned. Ask for an itemized, written breakdown and a receipt before paying anything.",
     "ফির কথা আছে - লিখিত বিস্তারিত হিসাব ও রসিদ ছাড়া টাকা দেবেন না।"),
    ("company_not_verifiable", "amber", 10,
     [r"company", r"কোম্পানি"],
     "A company is named. Verify it independently - search the company, call it directly, do not trust only the agent's documents.",
     "কোম্পানির নাম আছে - এজেন্টের কাগজের ওপর ভরসা না করে নিজে যাচাই করুন।"),
]

POSITIVE_PATTERNS = [
    (r"bmet", "BMET mentioned - check the recruiter's BMET licence number on the official BMET list."),
    (r"work visa", "Work visa (not tourist) mentioned - still verify the visa with the embassy."),
    (r"itemi[sz]ed", "Itemized breakdown mentioned - ask for it in writing before paying."),
    (r"receipt", "Receipt mentioned - insist on a proper receipt for every payment."),
    (r"interview", "Interview mentioned - a real process usually includes one."),
]

QUESTIONS = [
    "What is the recruiter's BMET licence number? Can I check it myself?",
    "Will I get a work visa (not tourist) and a written contract BEFORE I pay?",
    "Can I have an itemized fee breakdown and a receipt for every payment?",
    "Can I contact the employer directly, without the agent in between?",
    "What happens to my money if the visa is refused or the job does not exist?",
]


def check(text: str) -> dict:
    lowered = text.lower()
    flags = []
    score = 0
    for rule_id, level, weight, patterns, reason_en, reason_bn in RULES:
        for pat in patterns:
            if re.search(pat, lowered):
                flags.append({"id": rule_id, "level": level, "weight": weight,
                              "reason_en": reason_en, "reason_bn": reason_bn})
                score += weight
                break
    positives = []
    # Negation guard: "no receipt" / "no interview" must NOT count as positives.
    for pat, note in POSITIVE_PATTERNS:
        if pat == "receipt" and "no receipt" in lowered:
            continue
        if pat == "interview" and "no interview" in lowered:
            continue
        if re.search(pat, lowered):
            positives.append(note)
    score = min(100, score)
    if score >= 60:
        verdict, verdict_bn = "RED - DO NOT PAY YET", "লাল - এখনো টাকা দেবেন না"
        advice = "Stop. Do not pay, do not hand over your passport, and verify with BMET / the embassy / the employer directly first."
    elif score >= 30:
        verdict, verdict_bn = "AMBER - VERIFY FIRST", "হলুদ - আগে যাচাই করুন"
        advice = "Do not pay until you have checked the 5 questions below and verified the recruiter and employer independently."
    else:
        verdict, verdict_bn = "GREEN - LOW RISK ON THESE CHECKS ONLY", "সবুজ - এই পরীক্ষায় কম ঝুঁকি"
        advice = "No major red flags found in this text alone. That does NOT prove it is legitimate - still verify officially before paying."
    return {
        "score": score,
        "verdict": verdict,
        "verdict_bn": verdict_bn,
        "advice": advice,
        "flags": flags,
        "positives": positives,
        "questions": QUESTIONS,
        "disclaimer": "Not legal advice. Always verify with BMET, the embassy, and the employer directly. Never upload passport or bank details to this tool.",
    }
