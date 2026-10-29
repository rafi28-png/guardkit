// GuardKit Web: CheckFirst (message) + SafeOffer (offer), client-side only.
let lang = 'en';
function showTab(t) {
  document.getElementById('pane-msg').classList.toggle('hidden', t !== 'msg');
  document.getElementById('pane-offer').classList.toggle('hidden', t !== 'offer');
  document.getElementById('tab-msg').classList.toggle('active', t === 'msg');
  document.getElementById('tab-offer').classList.toggle('active', t === 'offer');
}
const UI = {
  en: {intro:"Worldwide trust checks in one app, in English — with Bengali support. Nothing is uploaded — checking happens in your browser.", details:"What is GuardKit? All seven tools at a glance", tabMsg:"✅ Check a Message (CheckFirst)", tabOffer:"💰 Check an Offer (SafeOffer)", labelMsg:"Paste a forwarded message here ", labelOffer:"Paste a job, loan, or deal offer here ", checkMsg:"Check this message", exampleMsg:"Load scam example", checkOffer:"Check this offer", exampleOffer:"Load fake job example", copy:"Copy summary", historyTitle:"Recent checks on this device (local only, never uploaded)", privacy:"Privacy: client-side only. Not legal advice, not a proof of truth. GuardKit is a worldwide project — verify with your local official authority, embassy, or employer directly. The other GuardKit tools (SemVer-Diff, TraceLock, WattShift, ShmPipe, SecretScan) are developer tools in their own folders — see the main README.", dark:"🌙 Dark", light:"☀️ Light"},
  bn: {intro:"একটি অ্যাপে দুটি বিশ্বাস-যাচাই, বাংলা ও ইংরেজিতে। কিছুই আপলোড হয় না — যাচাই আপনার ব্রাউজারেই হয়।", details:"GuardKit কী? সাতটি টুল এক নজরে", tabMsg:"✅ একটি মেসেজ যাচাই করুন (CheckFirst)", tabOffer:"💰 একটি অফার যাচাই করুন (SafeOffer)", labelMsg:"এখানে ফরওয়ার্ড করা মেসেজ পেস্ট করুন ", labelOffer:"এখানে চাকরি, ঋণ বা ডিলের অফার পেস্ট করুন ", checkMsg:"এই মেসেজটি যাচাই করুন", exampleMsg:"স্ক্যাম উদাহরণ লোড করুন", checkOffer:"এই অফারটি যাচাই করুন", exampleOffer:"ভুয়া চাকরির উদাহরণ লোড করুন", copy:"সারাংশ কপি করুন", historyTitle:"এই ডিভাইসে সাম্প্রতিক যাচাই (শুধু লোকাল, কখনো আপলোড হয় না)", privacy:"গোপনীয়তা: শুধু আপনার ব্রাউজারে চলে। আইনি পরামর্শ নয়, সত্যের প্রমাণ নয়। সবসময় BMET / দূতাবাস / নিয়োগকর্তার কাছে সরাসরি যাচাই করুন।", dark:"🌙 ডার্ক", light:"☀️ লাইট"}
};
function applyLang() {
  const t = UI[lang];
  const set = (id, txt) => { const el = document.getElementById(id); if (el) el.textContent = txt; };
  set('intro', t.intro); set('details-title', t.details); set('tab-msg', t.tabMsg); set('tab-offer', t.tabOffer);
  set('btn-check-msg', t.checkMsg); set('btn-example-msg', t.exampleMsg); set('btn-check-offer', t.checkOffer); set('btn-example-offer', t.exampleOffer);
  set('btn-copy', t.copy); set('history-title', t.historyTitle); set('privacy', t.privacy);
  document.getElementById('label-msg').childNodes[0].textContent = t.labelMsg;
  document.getElementById('label-offer').childNodes[0].textContent = t.labelOffer;
  renderHistory();
}
function setLang(l) {
  lang = l;
  document.getElementById('btn-en').classList.toggle('active', l === 'en');
  document.getElementById('btn-bn').classList.toggle('active', l === 'bn');
  document.documentElement.lang = l;
  applyLang();
  // Re-check whatever is already pasted, so verdicts switch language too.
  if (document.getElementById('msg').value.trim() && !document.getElementById('pane-msg').classList.contains('hidden')) checkMessage();
  if (document.getElementById('offer').value.trim() && !document.getElementById('pane-offer').classList.contains('hidden')) checkOffer();
}
document.getElementById('btn-en').onclick = () => setLang('en');
document.getElementById('btn-bn').onclick = () => setLang('bn');
document.getElementById('btn-dark').onclick = () => {
  const dark = document.body.classList.toggle('dark');
  document.getElementById('btn-dark').textContent = dark ? UI[lang].light : UI[lang].dark;
  try { localStorage.setItem('guardkit_dark', dark ? '1' : '0'); } catch (e) {}
};
try { if (localStorage.getItem('guardkit_dark') === '1') { document.body.classList.add('dark'); document.getElementById('btn-dark').textContent = '☀️ Light'; } } catch (e) {}
function copyShare(id) { navigator.clipboard.writeText(document.getElementById(id).textContent).then(() => alert('Copied!')); }
function shareWhatsApp(id) {
  const text = document.getElementById(id).textContent;
  window.open('https://wa.me/?text=' + encodeURIComponent(text), '_blank');
}
function clearPane(kind) {
  const id = kind === 'msg' ? 'msg' : 'offer';
  document.getElementById(id).value = '';
  document.getElementById(kind === 'msg' ? 'result-msg' : 'result-offer').classList.add('hidden');
  livePreview(id);
}
// Live preview + chips: interactive, before pressing Check.
function scoreText(text, rules) {
  let s = 0, flags = [];
  for (const r of rules) if (r.pats.some(p => p.test(text))) { s += r.w; flags.push(r); }
  return {score: Math.min(100, s), flags};
}
function livePreview(kind) {
  const id = kind === 'msg' ? 'msg' : 'offer';
  const text = document.getElementById(id).value;
  const el = document.getElementById(kind === 'msg' ? 'live-msg' : 'live-offer');
  if (!text.trim()) { el.innerHTML = lang === 'bn' ? 'টাইপ বা পেস্ট করুন — চেক বোতাম চাপার আগেই লাইভ ঝুঁকির পূর্বাভাস এখানে দেখা যাবে।' : 'Type or paste — your live risk preview will appear here, before you even press Check.'; return; }
  const {score, flags} = scoreText(text, kind === 'msg' ? MSG_RULES : OFFER_RULES);
  const color = score >= 60 ? '🔴' : score >= 30 ? '🟡' : '🟢';
  el.innerHTML = lang === 'bn'
    ? `${color} <strong>লাইভ পূর্বাভাস: ${score}/100</strong> — ${flags.length ? 'এখন পর্যন্ত ' + flags.length + 'টি লক্ষণ' : 'এখনো কোনো লক্ষণ নেই'}। পূর্ণ ফলাফলের জন্য চেক করুন।`
    : `${color} <strong>Live preview: ${score}/100</strong> — ${flags.length ? flags.length + ' flag(s) so far' : 'no flags yet'}. Press Check for the full verdict.`;
}
function tryChip(id, phrase) {
  const el = document.getElementById(id);
  el.value = (el.value ? el.value + ' ' : '') + phrase + '. ';
  el.focus();
  livePreview(id);
}
function setGauge(gaugeId, score, cls) {
  const g = document.getElementById(gaugeId);
  g.className = 'gauge ' + cls;
  // Animate: reset then set, so the bar grows on every check.
  g.querySelector('div').style.width = '0%';
  requestAnimationFrame(() => { setTimeout(() => { g.querySelector('div').style.width = score + '%'; }, 30); });
}
// History: local only (localStorage), never uploaded. Shows last 5 checks.
function saveHistory(kind, score, verdict) {
  try {
    const h = JSON.parse(localStorage.getItem('guardkit_history') || '[]');
    h.unshift({kind, score, verdict, time: new Date().toLocaleString()});
    localStorage.setItem('guardkit_history', JSON.stringify(h.slice(0, 5)));
    renderHistory();
  } catch (e) { /* private mode: ignore */ }
}
function renderHistory() {
  const el = document.getElementById('history');
  if (!el) return;
  try {
    const h = JSON.parse(localStorage.getItem('guardkit_history') || '[]');
    const kindBn = {Message: 'মেসেজ', Offer: 'অফার'};
    el.innerHTML = h.length ? h.map(x => `<li>${x.time} — ${lang === 'bn' ? (kindBn[x.kind] || x.kind) : x.kind}: ${x.verdict} (${x.score}/100)</li>`).join('') : (lang === 'bn' ? '<li>এই ডিভাইসে এখনো কোনো যাচাই হয়নি।</li>' : '<li>No checks yet on this device.</li>');
  } catch (e) { el.innerHTML = '<li>History unavailable.</li>'; }
}
function extractDomains(text) {
  const m = text.match(/https?:\/\/[^\s]+|(?:bit\.ly|tinyurl\.com|t\.co)\/[^\s]+/gi) || [];
  return [...new Set(m.map(u => {
    try { return new URL(u.startsWith('http') ? u : 'https://' + u).hostname; } catch (e) { return u; }
  }))];
}
document.addEventListener('DOMContentLoaded', renderHistory);

const MSG_RULES = [
  {w:30, pats:[/\botp\b/i, /ওটিপি/], en:"Asks for OTP. Real banks / bKash NEVER ask for OTP.", bn:"OTP চাওয়া হচ্ছে। আসল ব্যাংক / বিকাশ কখনো OTP চায় না।"},
  {w:25, pats:[/lottery/i, /you (have )?won/i, /লটারি/], en:"Claims you won a lottery / prize you never entered.", bn:"অংশ না নিয়েই লটারি জেতার দাবি।"},
  {w:25, pats:[/fee.*claim/i, /bkash.*fee/i], en:"Asks for a fee to claim a prize / loan.", bn:"পুরস্কার পেতে ফি চাওয়া হচ্ছে।"},
  {w:30, pats:[/cure.*cancer/i, /100%.*cure/i, /ক্যান্সার.*নিরাময়/], en:"Claims a simple cure for a serious disease.", bn:"গুরুতর রোগের সহজ নিরাময়ের দাবি।"},
  {w:15, pats:[/forward to \d+/i, /ফরওয়ার্ড করুন/], en:"Chain message asking you to forward to many people.", bn:"অনেককে ফরওয়ার্ড করতে বলা হচ্ছে।"},
  {w:15, pats:[/urgent/i, /today only/i, /জরুরি/], en:"Urgency pressure to stop you checking.", bn:"তাড়াহুড়ো করানো হচ্ছে।"},
  {w:15, pats:[/bit\.ly/i, /tinyurl/i], en:"Shortened link hides the real destination.", bn:"সংক্ষিপ্ত লিংক আসল ঠিকানা লুকায়।"},
  {w:20, pats:[/https?:\/\/\d+\.\d+\.\d+\.\d+/i], en:"Link goes to a raw IP address, not a named website — very suspicious.", bn:"লিংকটি কোনো ওয়েবসাইটের নাম নয়, সরাসরি IP ঠিকানায় যায় — খুব সন্দেহজনক।"},
  {w:20, pats:[/xn--/i], en:"Link uses punycode (xn--) — often used to fake a real site name.", bn:"লিংকে punycode (xn--) আছে — আসল সাইটের নাম নকল করতে ব্যবহৃত হয়।"},
  {w:20, pats:[/account.*closed/i, /অ্যাকাউন্ট.*বন্ধ/], en:"Threat that your account will be closed if you don't act now.", bn:"এখনই ব্যবস্থা না নিলে অ্যাকাউন্ট বন্ধের হুমকি।"},
];
const OFFER_RULES = [
  {w:30, pats:[/tourist visa/i, /ট্যুরিস্ট ভিসা/], en:"Job on a tourist visa - you could arrive jobless.", bn:"ট্যুরিস্ট ভিসায় চাকরি - পৌঁছে চাকরি নাও থাকতে পারে।"},
  {w:25, pats:[/cash/i, /no receipt/i, /নগদ/], en:"Cash with no receipt is almost impossible to recover.", bn:"রসিদ ছাড়া নগদ টাকা ফেরত পাওয়া প্রায় অসম্ভব।"},
  {w:25, pats:[/pay before/i, /advance.*fee/i, /আগে টাকা/], en:"Fee demanded before visa / contract.", bn:"ভিসা / চুক্তির আগেই টাকা চাওয়া হচ্ছে।"},
  {w:30, pats:[/passport.*kept/i, /পাসপোর্ট.*রাখ/], en:"Passport kept / confiscated - trafficking red flag.", bn:"পাসপোর্ট রেখে দেওয়া মানব পাচারের লক্ষণ।"},
  {w:20, pats:[/cambodia/i, /কম্বোডিয়া/], en:"Destination caution: Cambodia reported as scam-compound route.", bn:"কম্বোডিয়া সম্পর্কে সতর্কতা - বাড়তি যাচাই করুন।"},
  {w:20, pats:[/6 lakh/i, /৬ লাখ/], en:"Very large fee mentioned.", bn:"খুব বড় অঙ্কের ফি।"},
  {w:25, pats:[/work permit.*fee/i, /medical.*fee/i, /training.*fee/i, /ওয়ার্ক পারমিট.*ফি/], en:"Extra fee for work permit / medical / training before a contract.", bn:"চুক্তির আগে ওয়ার্ক পারমিট / মেডিকেল / ট্রেনিং ফি চাওয়া হচ্ছে।"},
];
const OFFER_QUESTIONS_EN = ["What is the recruiter's BMET licence number?", "Will I get a work visa and written contract BEFORE I pay?", "Can I have an itemized fee breakdown and a receipt?", "Can I contact the employer directly?", "What happens if the visa is refused?"];
const OFFER_QUESTIONS_BN = ["রিক্রুটারের BMET লাইসেন্স নম্বর কত?", "টাকা দেওয়ার আগেই কি আমি ওয়ার্ক ভিসা ও লিখিত চুক্তি পাব?", "ফির বিস্তারিত হিসাব ও রসিদ দিতে পারবেন?", "আমি কি সরাসরি নিয়োগকর্তার সঙ্গে কথা বলতে পারব?", "ভিসা বাতিল হলে কী হবে?"];

function verdictFor(score, kind) {
  if (score >= 60) return {cls:'red', en: kind === 'msg' ? 'RED - DO NOT FORWARD' : 'RED - DO NOT PAY YET', bn: kind === 'msg' ? 'লাল - ফরওয়ার্ড করবেন না' : 'লাল - এখনো টাকা দেবেন না'};
  if (score >= 30) return {cls:'amber', en:'AMBER - VERIFY FIRST', bn:'হলুদ - আগে যাচাই করুন'};
  return {cls:'green', en:'GREEN - NO MAJOR FLAGS FOUND', bn:'সবুজ - বড় ঝুঁকি পাওয়া যায়নি'};
}
function checkMessage() {
  const text = document.getElementById('msg').value;
  if (!text.trim()) return alert('Please paste a message first');
  let score = 0, flags = [];
  for (const r of MSG_RULES) if (r.pats.some(p => p.test(text))) { score += r.w; flags.push(r); }
  score = Math.min(100, score);
  const v = verdictFor(score, 'msg');
  document.getElementById('card-msg').className = 'card ' + v.cls;
  document.getElementById('score-msg').textContent = `Score: ${score}/100`;
  setGauge('gauge-msg', score, v.cls);
  document.getElementById('verdict-msg').textContent = lang === 'bn' ? v.bn : v.en;
  document.getElementById('advice-msg').textContent = lang === 'bn'
    ? (score >= 60 ? 'থামুন। ফরওয়ার্ড করবেন না, ক্লিক করবেন না, OTP বা টাকা পাঠাবেন না।' : 'ফরওয়ার্ড করার আগে অফিসিয়াল সূত্রে যাচাই করুন।')
    : (score >= 60 ? 'Stop. Do not forward, do not click, do not send OTP or money.' : 'Verify with an official source before forwarding.');
  document.getElementById('flags-msg').innerHTML = flags.length ? flags.map(f => `<li>${lang === 'bn' ? f.bn : f.en}</li>`).join('') : '<li>(none)</li>';
  document.getElementById('share-msg').textContent = lang === 'bn'
    ? `CheckFirst: ${v.bn} (স্কোর ${score}/100)। শেয়ার করার আগে আমি এই ফরওয়ার্ডটি যাচাই করেছি।`
    : `CheckFirst: ${v.en} (score ${score}/100). I checked this forward before sharing it.`;
  const domains = extractDomains(text);
  if (domains.length) document.getElementById('share-msg').textContent += ` Links found: ${domains.join(', ')} — check each domain yourself, do not click blindly.`;
  saveHistory('Message', score, lang === 'bn' ? v.bn : v.en);
  document.getElementById('result-msg').classList.remove('hidden');
}
function checkOffer() {
  const text = document.getElementById('offer').value;
  if (!text.trim()) return alert('Please paste an offer first');
  let score = 0, flags = [];
  for (const r of OFFER_RULES) if (r.pats.some(p => p.test(text))) { score += r.w; flags.push(r); }
  score = Math.min(100, score);
  const v = verdictFor(score, 'offer');
  document.getElementById('card-offer').className = 'card ' + v.cls;
  document.getElementById('score-offer').textContent = `Score: ${score}/100`;
  setGauge('gauge-offer', score, v.cls);
  document.getElementById('verdict-offer').textContent = lang === 'bn' ? v.bn : v.en;
  document.getElementById('advice-offer').textContent = lang === 'bn'
    ? (score >= 60 ? 'থামুন। টাকা দেবেন না, পাসপোর্ট দেবেন না। আগে BMET / দূতাবাস / নিয়োগকর্তার কাছে যাচাই করুন।' : 'টাকা দেওয়ার আগে অফিসিয়ালভাবে যাচাই করুন।')
    : (score >= 60 ? 'Stop. Do not pay, do not hand over your passport. Verify with BMET / embassy / employer first.' : 'Verify officially before paying.');
  document.getElementById('flags-offer').innerHTML = flags.length ? flags.map(f => `<li>${lang === 'bn' ? f.bn : f.en}</li>`).join('') : '<li>(none)</li>';
  document.getElementById('questions-offer').innerHTML = (lang === 'bn' ? OFFER_QUESTIONS_BN : OFFER_QUESTIONS_EN).map(q => `<li>${q}</li>`).join('');
  saveHistory('Offer', score, lang === 'bn' ? v.bn : v.en);
  document.getElementById('result-offer').classList.remove('hidden');
}
function loadMsgExample() { document.getElementById('msg').value = "Congratulations! You have won lottery 10 lakh taka! To claim your prize, send your OTP and pay a small bKash fee today only. Urgent! Click this link bit.ly/claim-now and send OTP to our bKash official number. Forward this to 10 people to activate."; checkMessage(); }
function loadOfferExample() { document.getElementById('offer').value = "URGENT! Last seat! Computer operator job in Cambodia, salary $1500 per month, no experience required, no interview. Quick departure today only. Pay 6 lakh taka cash now, no receipt, before visa. Tourist visa will be arranged. Passport will be kept by the company on arrival."; checkOffer(); }
