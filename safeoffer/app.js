// SafeOffer web checker - same rules as the Python version, client-side only.
// Nothing is uploaded. All checking happens in this browser.
let lang = 'en';

const RULES = [
  {id:'tourist', level:'red', w:30, pats:[/tourist visa/i, /visit visa/i, /ট্যুরিস্ট ভিসা/, /ভিজিট ভিসা/],
   en:"Job offered on a tourist / visit visa - you could arrive jobless and undocumented.",
   bn:"ট্যুরিস্ট / ভিজিট ভিসায় চাকরি - পৌঁছে চাকরি নাও থাকতে পারে।"},
  {id:'cash', level:'red', w:25, pats:[/cash/i, /no receipt/i, /নগদ/, /রসিদ ছাড়া/],
   en:"Payment in cash with no receipt is almost impossible to trace or recover.",
   bn:"রসিদ ছাড়া নগদ টাকা ফেরত পাওয়া প্রায় অসম্ভব।"},
  {id:'paybefore', level:'red', w:25, pats:[/pay before/i, /advance.*fee/i, /processing fee/i, /আগে টাকা/, /অগ্রিম/],
   en:"Fee demanded before a visa, offer letter, or contract is issued.",
   bn:"ভিসা / অফার লেটার পাওয়ার আগেই টাকা চাওয়া হচ্ছে।"},
  {id:'passport', level:'red', w:30, pats:[/passport.*kept/i, /passport.*confiscat/i, /পাসপোর্ট.*রাখ/],
   en:"Passport being kept / confiscated is a classic trafficking red flag.",
   bn:"পাসপোর্ট রেখে দেওয়া মানব পাচারের বড় লক্ষণ।"},
  {id:'highfee', level:'red', w:20, pats:[/6 lakh/i, /600,?000/, /900,?000/, /5 lakh/i, /৬ লাখ/, /৫ লাখ/],
   en:"Very large fee mentioned. Compare with the official fee and get an itemized breakdown.",
   bn:"খুব বড় অঙ্কের ফি - সরকারি ফির সঙ্গে মিলিয়ে দেখুন।"},
  {id:'cambodia', level:'red', w:20, pats:[/cambodia/i, /কম্বোডিয়া/],
   en:"Destination caution: Cambodia has been reported as a route for scam compounds. Verify extra carefully.",
   bn:"সতর্কতা: কম্বোডিয়া সম্পর্কে সাম্প্রতিক প্রতিবেদনে স্ক্যাম সেন্টারের কথা বলা হয়েছে।"},
  {id:'urgency', level:'amber', w:15, pats:[/urgent/i, /today only/i, /last seat/i, /জরুরি/, /আজই/],
   en:"Urgency pressure ('today only', 'last seat') is a common scam tactic.",
   bn:"তাড়াহুড়ো করানো স্ক্যামের সাধারণ কৌশল।"},
  {id:'noexp', level:'amber', w:15, pats:[/no experience/i, /no interview/i, /অভিজ্ঞতা লাগবে না/],
   en:"High salary with no experience and no interview - verify the employer really exists.",
   bn:"অভিজ্ঞতা / ইন্টারভিউ ছাড়া বেশি বেতন - নিয়োগকর্তা যাচাই করুন।"},
  {id:'personal', level:'amber', w:15, pats:[/bkash.*personal/i, /personal.*bkash/i, /personal number/i, /বিকাশ.*পার্সোনাল/],
   en:"Payment to a personal bKash / personal number, not a company bank account.",
   bn:"কোম্পানির ব্যাংক অ্যাকাউন্ট নয়, ব্যক্তিগত বিকাশে টাকা পাঠাতে বলা হচ্ছে।"},
  {id:'contractlater', level:'amber', w:15, pats:[/sign.*abroad/i, /sign.*after.*arriv/i, /পরে.*চুক্তি/],
   en:"Contract to be signed after arrival - risk of contract substitution with lower pay.",
   bn:"পৌঁছানোর পর চুক্তি সই - বেতন কমিয়ে দেওয়ার ঝুঁকি থাকে।"},
];

const QUESTIONS = {
  en: [
    "What is the recruiter's BMET licence number? Can I check it myself?",
    "Will I get a work visa (not tourist) and a written contract BEFORE I pay?",
    "Can I have an itemized fee breakdown and a receipt for every payment?",
    "Can I contact the employer directly, without the agent in between?",
    "What happens to my money if the visa is refused or the job does not exist?"
  ],
  bn: [
    "রিক্রুটারের BMET লাইসেন্স নম্বর কত? আমি নিজে যাচাই করতে পারব?",
    "টাকা দেওয়ার আগে কি ওয়ার্ক ভিসা (ট্যুরিস্ট নয়) ও লিখিত চুক্তি পাব?",
    "প্রতিটি পেমেন্টের বিস্তারিত হিসাব ও রসিদ পাব?",
    "এজেন্ট ছাড়া সরাসরি নিয়োগকর্তার সঙ্গে যোগাযোগ করতে পারব?",
    "ভিসা না হলে বা চাকরি না থাকলে আমার টাকার কী হবে?"
  ]
};

function setLang(l) {
  lang = l;
  document.getElementById('btn-en').classList.toggle('active', l === 'en');
  document.getElementById('btn-bn').classList.toggle('active', l === 'bn');
  document.querySelectorAll('[data-en]').forEach(el => {
    el.textContent = l === 'bn' ? el.dataset.bn : el.dataset.en;
  });
  const cur = document.getElementById('offer').value;
  if (cur.trim()) check();
}
document.getElementById('btn-en').onclick = () => setLang('en');
document.getElementById('btn-bn').onclick = () => setLang('bn');

function check() {
  const text = document.getElementById('offer').value;
  if (!text.trim()) { alert(lang === 'bn' ? 'প্রথমে অফারটি পেস্ট করুন' : 'Please paste an offer first'); return; }
  let score = 0, flags = [];
  for (const r of RULES) {
    if (r.pats.some(p => p.test(text))) { score += r.w; flags.push(r); }
  }
  score = Math.min(100, score);
  const card = document.getElementById('verdict-card');
  let verdict, advice, cls;
  if (score >= 60) {
    cls = 'red';
    verdict = lang === 'bn' ? 'লাল - এখনো টাকা দেবেন না' : 'RED - DO NOT PAY YET';
    advice = lang === 'bn' ? 'থামুন। টাকা দেবেন না, পাসপোর্ট দেবেন না, আগে BMET / দূতাবাস / নিয়োগকর্তার কাছে যাচাই করুন।'
      : 'Stop. Do not pay, do not hand over your passport, and verify with BMET / the embassy / the employer directly first.';
  } else if (score >= 30) {
    cls = 'amber';
    verdict = lang === 'bn' ? 'হলুদ - আগে যাচাই করুন' : 'AMBER - VERIFY FIRST';
    advice = lang === 'bn' ? 'নিচের ৫টি প্রশ্নের উত্তর না পাওয়া পর্যন্ত টাকা দেবেন না।'
      : 'Do not pay until you have checked the 5 questions below and verified independently.';
  } else {
    cls = 'green';
    verdict = lang === 'bn' ? 'সবুজ - এই পরীক্ষায় কম ঝুঁকি' : 'GREEN - LOW RISK ON THESE CHECKS ONLY';
    advice = lang === 'bn' ? 'এই লেখায় বড় ঝুঁকি পাওয়া যায়নি। তবে এটি বৈধতার প্রমাণ নয় - তবুও সরকারিভাবে যাচাই করুন।'
      : 'No major red flags found in this text alone. That does NOT prove it is legitimate - still verify officially before paying.';
  }
  card.className = cls;
  document.getElementById('score').textContent = `Score: ${score}/100`;
  document.getElementById('verdict').textContent = verdict;
  document.getElementById('advice').textContent = advice;
  document.getElementById('flags').innerHTML = flags.length
    ? flags.map(f => `<li>[${f.level}] ${lang === 'bn' ? f.bn : f.en}</li>`).join('')
    : '<li>(none found)</li>';
  document.getElementById('questions').innerHTML = QUESTIONS[lang].map(q => `<li>${q}</li>`).join('');
  document.getElementById('result').classList.remove('hidden');
}

document.getElementById('check').onclick = check;
document.getElementById('load-fake').onclick = () => {
  document.getElementById('offer').value = "URGENT! Last seat! Computer operator job in Cambodia, salary $1500 per month, no experience required, no interview. Quick departure today only. Pay 6 lakh taka cash now, no receipt, before visa. Tourist visa will be arranged. Passport will be kept by the company on arrival. Contact on WhatsApp personal number only.";
  check();
};
document.getElementById('load-legit').onclick = () => {
  document.getElementById('offer').value = "Licensed recruiter, BMET licence number to be verified on the official BMET list. Work visa (not tourist). Interview with the employer. Written contract in English and Bengali before any payment. Itemized fee breakdown with receipt for every payment. Company contact details provided so you can call the employer directly.";
  check();
};
document.getElementById('clear').onclick = () => {
  document.getElementById('offer').value = '';
  document.getElementById('result').classList.add('hidden');
};
