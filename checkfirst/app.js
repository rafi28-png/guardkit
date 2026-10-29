// CheckFirst web checker - same rules as Python version, client-side only.
let lang = 'en';
const RULES = [
  {id:'otp', level:'red', w:30, pats:[/\botp\b/i, /ওটিপি/],
   en:"Asks you to send/share an OTP. Real banks and bKash NEVER ask for your OTP.",
   bn:"OTP চাওয়া হচ্ছে। আসল ব্যাংক / বিকাশ কখনো OTP চায় না।"},
  {id:'lottery', level:'red', w:25, pats:[/lottery/i, /you (have )?won/i, /লটারি/],
   en:"Claims you won a lottery / prize you never entered.",
   bn:"অংশ না নিয়েই লটারি / পুরস্কার জেতার দাবি।"},
  {id:'fee', level:'red', w:25, pats:[/fee.*claim/i, /pay.*claim/i, /bkash.*fee/i],
   en:"Asks for a fee to claim a prize, loan, or offer.",
   bn:"পুরস্কার / ঋণ পেতে ফি চাওয়া হচ্ছে।"},
  {id:'cure', level:'red', w:30, pats:[/cure.*cancer/i, /cure.*diabetes/i, /100%.*cure/i, /ক্যান্সার.*নিরাময়/],
   en:"Claims a simple cure for a serious disease. Check with a doctor, do not stop treatment on this basis.",
   bn:"গুরুতর রোগের সহজ নিরাময়ের দাবি - ডাক্তারের সঙ্গে যাচাই করুন।"},
  {id:'guaranteed', level:'amber', w:15, pats:[/100% guaranteed/i, /scientists.*discover/i, /বিজ্ঞানীরা.*আবিষ্কার/],
   en:"Absolute guarantee / vague 'scientists say' with no named study or link.",
   bn:"১০০% গ্যারান্টি / নামহীন 'বিজ্ঞানীরা বলেছেন'।"},
  {id:'chain', level:'amber', w:15, pats:[/forward to \d+/i, /forward.*as received/i, /ফরওয়ার্ড করুন/],
   en:"Chain message asking you to forward to many people. This is how rumors spread.",
   bn:"অনেককে ফরওয়ার্ড করতে বলা হচ্ছে - এভাবেই গুজব ছড়ায়।"},
  {id:'urgency', level:'amber', w:15, pats:[/urgent/i, /today only/i, /account.*block/i, /জরুরি/, /আজই/],
   en:"Urgency / threat to stop you checking.",
   bn:"তাড়াহুড়ো / হুমকি দিয়ে যাচাই করতে বাধা দেওয়া হচ্ছে।"},
  {id:'shortlink', level:'amber', w:15, pats:[/bit\.ly/i, /tinyurl/i, /t\.co\//i],
   en:"Uses a shortened link that hides the real destination.",
   bn:"সংক্ষিপ্ত লিংক আসল ঠিকানা লুকায়।"},
  {id:'impersonation', level:'amber', w:15, pats:[/bkash official/i, /bank official/i, /বিকাশ.*অফিসিয়াল/],
   en:"Claims to be from a bank / bKash / government. Verify via the official app / number you already know.",
   bn:"ব্যাংক / বিকাশ / সরকারি বলে দাবি - আপনার জানা অফিসিয়াল নম্বরে যাচাই করুন।"},
];
const TODO = {
  en: ["Do NOT send OTP, money, or personal details.", "Do NOT click the link in the message. Go to the official app / website yourself.", "Do NOT forward it yet.", "Verify with an official / reputable source, and report it in the app."],
  bn: ["OTP, টাকা বা ব্যক্তিগত তথ্য পাঠাবেন না।", "মেসেজের লিংকে ক্লিক করবেন না। নিজে অফিসিয়াল অ্যাপ / ওয়েবসাইটে যান।", "এখনো ফরওয়ার্ড করবেন না।", "অফিসিয়াল সূত্রে যাচাই করুন এবং অ্যাপে রিপোর্ট করুন।"]
};
function setLang(l) {
  lang = l;
  document.getElementById('btn-en').classList.toggle('active', l === 'en');
  document.getElementById('btn-bn').classList.toggle('active', l === 'bn');
  document.querySelectorAll('[data-en]').forEach(el => { el.textContent = l === 'bn' ? el.dataset.bn : el.dataset.en; });
  if (document.getElementById('msg').value.trim()) check();
}
document.getElementById('btn-en').onclick = () => setLang('en');
document.getElementById('btn-bn').onclick = () => setLang('bn');
function check() {
  const text = document.getElementById('msg').value;
  if (!text.trim()) { alert(lang === 'bn' ? 'প্রথমে মেসেজটি পেস্ট করুন' : 'Please paste a message first'); return; }
  let score = 0, flags = [];
  for (const r of RULES) if (r.pats.some(p => p.test(text))) { score += r.w; flags.push(r); }
  score = Math.min(100, score);
  const card = document.getElementById('verdict-card');
  let verdict, advice, cls;
  if (score >= 60) { cls = 'red';
    verdict = lang === 'bn' ? 'লাল - সম্ভবত স্ক্যাম / ভুল তথ্য - ফরওয়ার্ড করবেন না' : 'RED - LIKELY SCAM / MISINFORMATION - DO NOT FORWARD';
    advice = lang === 'bn' ? 'থামুন। ফরওয়ার্ড করবেন না, ক্লিক করবেন না, OTP / টাকা পাঠাবেন না।' : 'Stop. Do not forward, do not click, do not send OTP or money.';
  } else if (score >= 30) { cls = 'amber';
    verdict = lang === 'bn' ? 'হলুদ - সন্দেহজনক - আগে যাচাই করুন' : 'AMBER - SUSPICIOUS - VERIFY FIRST';
    advice = lang === 'bn' ? 'এখনো ফরওয়ার্ড করবেন না। অফিসিয়াল সূত্রে যাচাই করুন।' : 'Do not forward yet. Verify with an official source first.';
  } else { cls = 'green';
    verdict = lang === 'bn' ? 'সবুজ - বড় কোনো সন্দেহজনক লক্ষণ পাওয়া যায়নি' : 'GREEN - NO MAJOR FLAGS FOUND';
    advice = lang === 'bn' ? 'এই লেখায় বড় ঝুঁকি পাওয়া যায়নি। তবে এটি সত্যের প্রমাণ নয় - সূত্র যাচাই করুন।' : 'No major flags found in this text alone. That does NOT prove it is true - still check the source before forwarding.';
  }
  card.className = cls;
  document.getElementById('score').textContent = `Score: ${score}/100`;
  document.getElementById('verdict').textContent = verdict;
  document.getElementById('advice').textContent = advice;
  document.getElementById('flags').innerHTML = flags.length ? flags.map(f => `<li>[${f.level}] ${lang === 'bn' ? f.bn : f.en}</li>`).join('') : '<li>(none found)</li>';
  document.getElementById('todo').innerHTML = TODO[lang].map(t => `<li>${t}</li>`).join('');
  const share = `CheckFirst: ${verdict} (score ${score}/100). ${advice} I checked this forward before sharing it.`;
  document.getElementById('share').textContent = share;
  document.getElementById('copy').onclick = () => navigator.clipboard.writeText(share).then(() => alert(lang === 'bn' ? 'কপি হয়েছে' : 'Copied!'));
  document.getElementById('result').classList.remove('hidden');
}
document.getElementById('check').onclick = check;
document.getElementById('load-scam').onclick = () => { document.getElementById('msg').value = "Congratulations! You have won lottery 10 lakh taka! To claim your prize, send your OTP and pay a small bKash fee today only. Urgent! Click this link bit.ly/claim-now and send OTP to our bKash official number. Forward this to 10 people to activate."; check(); };
document.getElementById('load-health').onclick = () => { document.getElementById('msg').value = "Breaking news! Scientists say drinking this herbal mix cures cancer in 3 days, 100% guaranteed. No doctor needed. Forward this to 10 people, forwarded as received. Scientists discover this secret cure."; check(); };
document.getElementById('load-legit').onclick = () => { document.getElementById('msg').value = "Official notice from Bangladesh Bank, published on https://www.bb.org.bd with date 29 October 2026, about new guidelines for mobile banking. Please read the full notice on the official website."; check(); };
document.getElementById('clear').onclick = () => { document.getElementById('msg').value = ''; document.getElementById('result').classList.add('hidden'); };
