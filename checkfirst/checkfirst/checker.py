"""CheckFirst checker: explainable, rule-based, no AI, no uploads.

For forwarded messages, not for job-payment decisions (see SafeOffer).
It does NOT prove a message true or false. It flags patterns that
make a message suspicious, and tells you what to verify before
forwarding, clicking, or sending money/OTP.

Score >= 60 = RED (Likely scam / misinformation - do not forward)
30-59 = AMBER (Suspicious - verify first)
Below 30 = GREEN (No major flags found - still not proof it is true)
"""
import re

# id, level, weight, category, patterns, reason_en, reason_bn
RULES = [
    ("otp_request", "red", 30, "scam",
     [r"\botp\b", r"otp.*send", r"otp.*share", r"ওটিপি"],
     "Asks you to send/share an OTP. Real banks and bKash NEVER ask for your OTP.",
     "OTP চাওয়া হচ্ছে। আসল ব্যাংক / বিকাশ কখনো OTP চায় না।"),
    ("lottery_prize", "red", 25, "scam",
     [r"lottery", r"you (have )?won", r"congratulations.*won", r"prize.*claim", r"লটারি", r"পুরস্কার.*জিত"],
     "Claims you won a lottery / prize you never entered - a classic scam opening.",
     "অংশ না নিয়েই লটারি / পুরস্কার জেতার দাবি - স্ক্যামের সাধারণ শুরু।"),
    ("fee_to_claim", "red", 25, "scam",
     [r"fee.*claim", r"pay.*claim", r"bkash.*fee", r"send.*fee", r"টাকা.*দাবি", r"ফি.*দিলে"],
     "Asks for a fee to claim a prize, loan, or offer. Legitimate prizes do not work this way.",
     "পুরস্কার / ঋণ পেতে ফি চাওয়া হচ্ছে - বৈধ পুরস্কারে এমন হয় না।"),
    ("health_cure", "red", 30, "misinformation",
     [r"cure.*cancer", r"cure.*diabetes", r"cures.*\bin \d+ days", r"100%.*cure", r"ক্যান্সার.*নিরাময়", r"৩ দিনে.*সার"],
     "Claims a simple cure for a serious disease, often in days and with 100% guarantee. Check with a doctor / official health source, do not stop treatment on this basis.",
     "গুরুতর রোগের সহজ নিরাময়ের দাবি - ডাক্তার / সরকারি স্বাস্থ্য সূত্র ছাড়া বিশ্বাস করবেন না।"),
    ("guaranteed_claim", "amber", 15, "misinformation",
     [r"100% guaranteed", r"guaranteed.*cure", r"scientists.*discover", r"১০০%.*গ্যারান্টি", r"বিজ্ঞানীরা.*আবিষ্কার"],
     "Absolute guarantee / vague 'scientists say' with no named study, journal, or link.",
     "১০০% গ্যারান্টি / নামহীন 'বিজ্ঞানীরা বলেছেন' - কোনো গবেষণা বা লিংক নেই।"),
    ("chain_forward", "amber", 15, "misinformation",
     [r"forward to \d+", r"forward.*as received", r"forward this", r"\d+ জনকে.*পাঠান", r"ফরওয়ার্ড করুন"],
     "Chain message asking you to forward to many people. This is how rumors spread, not how news is verified.",
     "অনেককে ফরওয়ার্ড করতে বলা হচ্ছে - এভাবেই গুজব ছড়ায়, খবর যাচাই হয় না।"),
    ("urgency", "amber", 15, "scam",
     [r"urgent", r"today only", r"account.*block", r"account.*clos", r"জরুরি", r"আজই", r"অ্যাকাউন্ট.*বন্ধ"],
     "Urgency / threat ('account will be blocked today') to stop you checking.",
     "তাড়াহুড়ো / হুমকি ('আজই অ্যাকাউন্ট বন্ধ হবে') - যাচাই করার সময় দেওয়া হচ্ছে না।"),
    ("short_link", "amber", 15, "scam",
     [r"bit\.ly", r"tinyurl", r"t\.co/", r"shorturl", r"bitly"],
     "Uses a shortened link that hides the real destination. Do not click blindly - expand / verify the destination first.",
     "সংক্ষিপ্ত লিংক আসল ঠিকানা লুকায় - না যাচাই করে ক্লিক করবেন না।"),
    ("impersonation", "amber", 15, "scam",
     [r"bkash official", r"bank official", r"government scheme", r"বিকাশ.*অফিসিয়াল", r"সরকারি.*প্রকল্প"],
     "Claims to be from a bank / bKash / government and asks you to click or pay. Verify via the official app / number you already know, not the number in the message.",
     "ব্যাংক / বিকাশ / সরকারি বলে দাবি - মেসেজের নম্বর নয়, আপনার জানা অফিসিয়াল নম্বরে যাচাই করুন।"),
    ("no_source", "amber", 10, "misinformation",
     [r"breaking news", r"scientists say", r"ব্রেকিং নিউজ", r"বিজ্ঞানীরা বলেছেন"],
     "Big claim with no named source, date, or official link. A real news story can be traced to a source.",
     "বড় দাবি, কিন্তু কোনো সূত্র, তারিখ বা অফিসিয়াল লিংক নেই।"),
    ("suspicious_link", "amber", 10, "scam",
     [r"https?://\d+\.\d+\.\d+\.\d+", r"http://[^\s]+"],
     "Contains a link, especially an IP-address link or plain http (not https). Check the domain carefully before clicking.",
     "লিংক আছে - ডোমেইন ভালো করে দেখুন, অপরিচিত লিংকে ক্লিক করবেন না।"),
    ("punycode_link", "amber", 20, "scam",
     [r"xn--"],
     "Link uses punycode (xn--) — often used to fake a real site name with look-alike characters.",
     "লিংকে punycode (xn--) আছে — আসল সাইটের নাম নকল করতে ব্যবহৃত হয়।"),
]

POSITIVE_PATTERNS = [
    (r"\.gov\.bd", "Links to a .gov.bd official domain - a good sign, still check the exact page."),
    (r"bb\.org\.bd|bangladeshbank", "Mentions Bangladesh Bank / official source - verify on the official site."),
    (r"https://", "Uses https links - better than plain http, but https alone does not prove legitimacy."),
]

WHAT_TO_DO = {
    "scam": [
        "Do NOT send OTP, money, or personal details.",
        "Do NOT click the link in the message. Go to the official app / website yourself.",
        "Do NOT forward it. Forwarding spreads the scam.",
        "Report it in the app (WhatsApp / Facebook) and warn the sender.",
    ],
    "misinformation": [
        "Do NOT forward it yet.",
        "Search the claim on an official / reputable news or health source.",
        "Check the date - old photos and old news are often reused as if new.",
        "If it is about health, ask a doctor - do not change treatment based on a forward.",
    ],
    "general": [
        "Verify with an official source you find yourself, not a link in the message.",
        "If in doubt, do not forward, do not click, do not pay.",
    ],
}


def check(text: str) -> dict:
    lowered = text.lower()
    flags = []
    score = 0
    categories = set()
    for rule_id, level, weight, cat, patterns, reason_en, reason_bn in RULES:
        for pat in patterns:
            if re.search(pat, lowered):
                flags.append({"id": rule_id, "level": level, "weight": weight, "category": cat,
                              "reason_en": reason_en, "reason_bn": reason_bn})
                score += weight
                categories.add(cat)
                break
    positives = []
    for pat, note in POSITIVE_PATTERNS:
        if re.search(pat, lowered):
            positives.append(note)
    score = min(100, score)
    if score >= 60:
        kind = "scam" if "scam" in categories and "misinformation" not in categories else "misinformation" if categories == {"misinformation"} else "scam"
        verdict = "RED - LIKELY SCAM / MISINFORMATION - DO NOT FORWARD"
        verdict_bn = "লাল - সম্ভবত স্ক্যাম / ভুল তথ্য - ফরওয়ার্ড করবেন না"
        advice = "Stop. Do not forward, do not click, do not send OTP or money."
    elif score >= 30:
        kind = "general"
        verdict = "AMBER - SUSPICIOUS - VERIFY FIRST"
        verdict_bn = "হলুদ - সন্দেহজনক - আগে যাচাই করুন"
        advice = "Do not forward yet. Verify with an official source first."
    else:
        kind = "general"
        verdict = "GREEN - NO MAJOR FLAGS FOUND"
        verdict_bn = "সবুজ - বড় কোনো সন্দেহজনক লক্ষণ পাওয়া যায়নি"
        advice = "No major flags found in this text alone. That does NOT prove it is true - still check the source before forwarding."
    return {
        "score": score,
        "verdict": verdict,
        "verdict_bn": verdict_bn,
        "advice": advice,
        "flags": flags,
        "positives": positives,
        "what_to_do": WHAT_TO_DO.get(kind, WHAT_TO_DO["general"]),
        "share_text": f"CheckFirst: {verdict} (score {score}/100). {advice} I checked this forward before sharing it.",
        "disclaimer": "Not a fact-check verdict. This flags patterns, it does not prove truth. Always verify with an official / reputable source. Never share OTP, passwords, or bank details.",
    }
