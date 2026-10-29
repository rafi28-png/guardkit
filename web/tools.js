// GuardKit Web — live browser versions of the 5 remaining tools.
// Pure client-side only. Nothing is uploaded. Core functions are pure and
// testable in Node; DOM handlers are only wired when document exists.
// Safety notes are honest: SecretScan never echoes a secret value, and
// SemVer-Diff Web runs code YOU paste, in YOUR browser — never paste
// untrusted code you have not read.

function gkEscape(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
  });
}

// ---------- 1. SecretScan ----------
const SECRET_PATTERNS = [
  {type: 'AWS access key', re: /AKIA[0-9A-Z]{16}/g},
  {type: 'GitHub token', re: /(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}/g},
  {type: 'Slack token', re: /xox[baprs]-[A-Za-z0-9-]{10,}/g},
  {type: 'Private key block', re: /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/g},
  {type: 'Generic password / API-key assignment', re: /\b(?:password|passwd|pwd|api_key|apikey|secret|token)\s*[:=]\s*["'][^"'\n]+["']|\b(?:password|passwd|pwd|api_key|apikey|secret|token)\s*[:=]\s*[^\s"'\n]+/gi},
];
function scanSecrets(text) {
  const findings = [];
  const lines = String(text || '').split(/\n/);
  lines.forEach(function (line, idx) {
    if (line.indexOf('secretscan:ignore') !== -1) return;
    let specificFound = false;
    SECRET_PATTERNS.forEach(function (p) {
      const isGeneric = p.type.indexOf('Generic') === 0;
      // A specific token (AWS/GitHub/Slack/key) on a line is reported once,
      // not again as a generic assignment on the same line.
      if (isGeneric && specificFound) return;
      p.re.lastIndex = 0;
      if (p.re.test(line)) {
        // Never echo the matched secret: only type + line + redaction.
        findings.push({type: p.type, line: idx + 1, value: '***'});
        if (!isGeneric) specificFound = true;
      }
    });
  });
  return findings;
}

// ---------- 2. SemVer-Diff Web (JavaScript functions) ----------
function parseJSFunction(code) {
  const src = String(code || '').trim();
  const m = src.match(/function\s+\w*\s*\(([^)]*)\)\s*\{([\s\S]*)\}$/);
  if (m) {
    const params = m[1].split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    return new Function(...params, m[2]);
  }
  // Fallback: body with arguments a, b.
  return new Function('a', 'b', src);
}
function parseInputs(raw) {
  const groups = String(raw || '').split(/[|\n;]+/).map(function (s) { return s.trim(); }).filter(Boolean);
  return groups.map(function (g) {
    return g.split(',').map(function (v) {
      v = v.trim();
      if (v === '') return v;
      const n = Number(v);
      return Number.isNaN(n) ? v.replace(/^["']|["']$/g, '') : n;
    });
  });
}
function runOne(fn, args) {
  try { return {ok: true, value: fn(...args)}; }
  catch (e) { return {ok: false, value: 'Error: ' + (e && e.message ? e.message : String(e))}; }
}
function fmtVal(v) {
  if (typeof v === 'number') return Number.isInteger(v) ? String(v) : String(Math.round(v * 1000000) / 1000000);
  return JSON.stringify(v);
}
function diffFunctions(oldCode, newCode, inputsRaw) {
  let oldFn, newFn;
  try { oldFn = parseJSFunction(oldCode); } catch (e) { return {error: 'OLD function could not be built: ' + e.message}; }
  try { newFn = parseJSFunction(newCode); } catch (e) { return {error: 'NEW function could not be built: ' + e.message}; }
  const inputs = parseInputs(inputsRaw);
  if (!inputs.length) return {error: 'Give at least one test input, e.g. 1,2 | 3,4'};
  const results = inputs.map(function (args) {
    const o = runOne(oldFn, args), n = runOne(newFn, args);
    const same = o.ok === n.ok && fmtVal(o.value) === fmtVal(n.value);
    return {input: args, old: o, new: n, divergence: !same};
  });
  return {results: results, divergences: results.filter(function (r) { return r.divergence; }).length};
}

// ---------- 3. TraceLock Web (CSV) ----------
function parseCSV(text) {
  const rows = [];
  let row = [], cur = '', inQ = false;
  const src = String(text || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  for (let i = 0; i < src.length; i++) {
    const c = src[i];
    if (inQ) {
      if (c === '"') {
        if (src[i + 1] === '"') { cur += '"'; i++; } else inQ = false;
      } else cur += c;
    } else if (c === '"') inQ = true;
    else if (c === ',') { row.push(cur); cur = ''; }
    else if (c === '\n') { row.push(cur); rows.push(row); row = []; cur = ''; }
    else cur += c;
  }
  if (cur !== '' || row.length) { row.push(cur); rows.push(row); }
  return rows.filter(function (r) { return !(r.length === 1 && r[0] === ''); });
}
function csvStats(text) {
  const rows = parseCSV(text);
  if (!rows.length) return {rows: 0, cols: 0, cells: 0, empty: 0, emptyPct: 0};
  const cols = Math.max(...rows.map(function (r) { return r.length; }));
  const data = rows.slice(1);
  let cells = 0, empty = 0;
  data.forEach(function (r) {
    for (let c = 0; c < cols; c++) { cells++; if ((r[c] || '').trim() === '') empty++; }
  });
  return {rows: data.length, cols: cols, cells: cells, empty: empty, emptyPct: cells ? (empty / cells) * 100 : 0};
}
async function sha256Hex(text) {
  const cryptoObj = (typeof crypto !== 'undefined' && crypto.subtle) ? crypto : (typeof globalThis !== 'undefined' && globalThis.crypto && globalThis.crypto.subtle ? globalThis.crypto : null);
  if (!cryptoObj) throw new Error('SHA-256 is not available in this environment');
  const buf = await cryptoObj.subtle.digest('SHA-256', new TextEncoder().encode(String(text || '')));
  return Array.from(new Uint8Array(buf)).map(function (b) { return b.toString(16).padStart(2, '0'); }).join('');
}
async function traceCSV(beforeText, afterText) {
  const b = csvStats(beforeText), a = csvStats(afterText);
  const bh = await sha256Hex(beforeText), ah = await sha256Hex(afterText);
  const alerts = [];
  if (bh !== ah) alerts.push('Content changed (SHA-256 differs).');
  if (a.emptyPct - b.emptyPct >= 10) alerts.push('Empty-cell % jumped by ' + (a.emptyPct - b.emptyPct).toFixed(1) + ' points.');
  if (a.emptyPct >= 50) alerts.push('After file is ' + a.emptyPct.toFixed(1) + '% empty cells.');
  if (a.rows !== b.rows) alerts.push('Row count changed: ' + b.rows + ' → ' + a.rows + '.');
  return {before: b, after: a, beforeHash: bh, afterHash: ah, changed: bh !== ah, alerts: alerts};
}

// ---------- 4. WattShift Web (live UK Carbon Intensity API) ----------
function parseCarbonForecast(api) {
  const data = (api && api.data) || [];
  if (!data.length) throw new Error('API returned no forecast data');
  const now = Date.now();
  let current = data[0];
  data.forEach(function (d) {
    const from = Date.parse(d.from), to = Date.parse(d.to);
    if (from <= now && now < to) current = d;
  });
  let best = data[0];
  data.forEach(function (d) { if (d.intensity.forecast < best.intensity.forecast) best = d; });
  return {current: current, best: best, slots: data.length};
}
async function wattShift(kwh) {
  // Correct live endpoint (verified 2026-10-30): /intensity/<now UTC>/fw24h.
  // The bare /intensity/forecast path returns HTTP 400 from this API.
  const now = new Date().toISOString().slice(0, 16) + 'Z';
  const res = await fetch('https://api.carbonintensity.org.uk/intensity/' + now + '/fw24h');
  if (!res.ok) throw new Error('Carbon Intensity API returned HTTP ' + res.status);
  const api = await res.json();
  const p = parseCarbonForecast(api);
  const cur = p.current.intensity.forecast, best = p.best.intensity.forecast;
  return {current: cur, best: best, currentFrom: p.current.from, bestFrom: p.best.from, savedG: Math.max(0, (cur - best) * kwh), kwh: kwh, slots: p.slots};
}

// ---------- 5. ShmPipe Web (CSV vs binary, in-browser) ----------
function shmBenchmark(n) {
  n = Math.max(1, Math.floor(n));
  const ids = new Int32Array(n), vals = new Float64Array(n);
  for (let i = 0; i < n; i++) { ids[i] = i + 1; vals[i] = (i * 1.5) + 0.25; }
  // CSV path: build string, then parse it back.
  const t0 = performance.now();
  let csv = 'id,value\n';
  for (let i = 0; i < n; i++) csv += ids[i] + ',' + vals[i] + '\n';
  const lines = csv.trim().split('\n').slice(1);
  let csvCount = 0, csvFirst = null, csvLast = null;
  lines.forEach(function (ln) {
    const parts = ln.split(',');
    const id = parseInt(parts[0], 10), v = parseFloat(parts[1]);
    if (csvCount === 0) csvFirst = [id, v];
    csvLast = [id, v]; csvCount++;
  });
  const csvMs = performance.now() - t0;
  // Binary path: pack both typed arrays into one ArrayBuffer, unpack again.
  const t1 = performance.now();
  const buf = new ArrayBuffer(n * 4 + n * 8);
  new Int32Array(buf, 0, n).set(ids);
  new Float64Array(buf, n * 4, n).set(vals);
  // .slice() copies the data back out — a view alone would not be a real round-trip.
  const rIds = new Int32Array(buf, 0, n).slice(), rVals = new Float64Array(buf, n * 4, n).slice();
  const binMs = performance.now() - t1;
  const ok = csvCount === n && rIds[0] === 1 && rVals[0] === 0.25 &&
    rIds[n - 1] === n && Math.abs(rVals[n - 1] - ((n - 1) * 1.5 + 0.25)) < 1e-9 &&
    csvFirst[0] === 1 && csvLast[0] === n;
  return {n: n, csvMs: csvMs, binMs: binMs, speedup: binMs > 0 ? csvMs / binMs : 0, ok: ok, first: [rIds[0], rVals[0]], last: [rIds[n - 1], rVals[n - 1]], csvCount: csvCount};
}

// ---------- DOM handlers (browser only) ----------
function gkOut(id, html) { const el = document.getElementById(id); if (el) el.innerHTML = html; }
function gkVal(id) { const el = document.getElementById(id); return el ? el.value : ''; }
function gkFileText(id) {
  const el = document.getElementById(id);
  if (!el || !el.files || !el.files[0]) return Promise.resolve('');
  return el.files[0].text();
}
function runSecretScan() {
  const text = gkVal('ss-input');
  if (!text.trim()) { gkOut('ss-out', '<p>Please paste code or config first.</p>'); return; }
  const f = scanSecrets(text);
  const cls = f.length ? 'red' : 'green';
  const verdict = f.length ? 'RED — ' + f.length + ' finding(s). Do NOT push this.' : 'GREEN — 0 findings in this input.';
  gkOut('ss-out', '<div class="card ' + cls + '"><h2>' + verdict + '</h2><p>Values are never shown — only type and line, with ***.</p></div>' +
    (f.length ? '<ul>' + f.map(function (x) { return '<li>Line ' + x.line + ': ' + gkEscape(x.type) + ' — ***</li>'; }).join('') + '</ul>' : '<p>No secrets found. This scans the patterns listed below; it cannot prove a file is safe.</p>'));
}
function loadSecretExample() {
  document.getElementById('ss-input').value = "aws_key = \"AKIAIOSFODNN7EXAMPLE\"\npassword = \"hunter2\"\n# clean line below\nname = \"guardkit\"\n";
  runSecretScan();
}
function runSemVerWeb() {
  const r = diffFunctions(gkVal('sv-old'), gkVal('sv-new'), gkVal('sv-inputs'));
  if (r.error) { gkOut('sv-out', '<p>' + gkEscape(r.error) + '</p>'); return; }
  const cls = r.divergences ? 'red' : 'green';
  const verdict = r.divergences ? 'BEHAVIOR CHANGE DETECTED — ' + r.divergences + ' divergence(s)' : 'No divergences on these inputs — patch looks safe on these inputs only.';
  gkOut('sv-out', '<div class="card ' + cls + '"><h2>' + verdict + '</h2></div><ul>' + r.results.map(function (x) {
    return '<li>Input (' + gkEscape(x.input.join(', ')) + '): old = ' + gkEscape(x.old.ok ? fmtVal(x.old.value) : x.old.value) +
      ' | new = ' + gkEscape(x.new.ok ? fmtVal(x.new.value) : x.new.value) + (x.divergence ? ' <strong>← DIVERGENCE</strong>' : '') + '</li>';
  }).join('') + '</ul><p class="privacy">Web version works on JavaScript functions; the full Python AST version is in the repo (semver-diff/). Only run code you have read — never paste untrusted code here.</p>');
}
function loadSemVerExample() {
  // Genuine divergence: trunc drops .5, round rounds it up.
  document.getElementById('sv-old').value = 'function round_half(x){ return Math.trunc(x); }';
  document.getElementById('sv-new').value = 'function round_half(x){ return Math.round(x); }';
  document.getElementById('sv-inputs').value = '2.5 | 3.5 | 2.0';
  runSemVerWeb();
}
async function runTraceWeb() {
  const before = await gkFileText('tl-before');
  const after = await gkFileText('tl-after');
  if (!before && !after) { gkOut('tl-out', '<p>Please choose a before-CSV and an after-CSV file first. Files are read in your browser only, never uploaded.</p>'); return; }
  try {
    const r = await traceCSV(before, after);
    const cls = r.alerts.length ? 'red' : 'green';
    gkOut('tl-out', '<div class="card ' + cls + '"><h2>' + (r.alerts.length ? 'ALERT — ' + r.alerts.length + ' issue(s)' : 'No alerts on these files') + '</h2></div>' +
      '<p>Before: ' + r.before.rows + ' rows, ' + r.before.cols + ' cols, ' + r.before.emptyPct.toFixed(1) + '% empty. SHA-256: ' + r.beforeHash.slice(0, 16) + '…</p>' +
      '<p>After: ' + r.after.rows + ' rows, ' + r.after.cols + ' cols, ' + r.after.emptyPct.toFixed(1) + '% empty. SHA-256: ' + r.afterHash.slice(0, 16) + '…</p>' +
      '<p>Content changed: ' + (r.changed ? 'yes' : 'no') + '</p>' +
      (r.alerts.length ? '<ul>' + r.alerts.map(function (a) { return '<li>' + gkEscape(a) + '</li>'; }).join('') + '</ul>' : '') +
      '<p class="privacy">Web version works on CSV files in your browser; full pipeline version is in the repo (tracelock/). Full hashes are not printed here — only the first 16 characters, to keep the report readable.</p>');
  } catch (e) { gkOut('tl-out', '<p>Could not hash files: ' + gkEscape(e.message) + '</p>'); }
}
async function runWattWeb() {
  const kwh = parseFloat(gkVal('ws-kwh')) || 2;
  gkOut('ws-out', '<p>Fetching live forecast from the UK Carbon Intensity API…</p>');
  try {
    const r = await wattShift(kwh);
    gkOut('ws-out', '<div class="card green"><h2>Live forecast — source: api.carbonintensity.org.uk</h2>' +
      '<p>Current slot (' + gkEscape(r.currentFrom) + '): ' + r.current + ' gCO₂/kWh</p>' +
      '<p>Best slot in forecast (' + gkEscape(r.bestFrom) + '): ' + r.best + ' gCO₂/kWh</p>' +
      '<p>For ' + r.kwh + ' kWh, waiting for the best slot would save about ' + r.savedG.toFixed(1) + ' g CO₂.</p>' +
      '<p class="privacy">Live data, ' + r.slots + ' forecast slots received. If the API is down, no live claim is made.</p></div>');
  } catch (e) {
    gkOut('ws-out', '<div class="card amber"><h2>Live data unavailable</h2><p>Could not fetch the UK Carbon Intensity API: ' + gkEscape(e.message) + '. No live numbers are shown, and no fallback numbers are presented as live data.</p>' +
      '<button onclick="showWattExample()">Show a labelled example (not live)</button><div id="ws-example"></div></div>');
  }
}
function showWattExample() {
  gkOut('ws-example', '<p><strong>ILLUSTRATIVE EXAMPLE — NOT LIVE DATA:</strong> if current were 290 and best were 115 gCO₂/kWh, then 2 kWh would save (290−115)×2 = 350 g. This is only an example of the calculation, not today\'s forecast.</p>');
}
function runShmWeb() {
  const sel = document.getElementById('shm-n');
  const n = sel ? parseInt(sel.value, 10) : 100000;
  gkOut('shm-out', '<p>Running in your browser…</p>');
  setTimeout(function () {
    const r = shmBenchmark(n);
    gkOut('shm-out', '<div class="card ' + (r.ok ? 'green' : 'red') + '"><h2>' + (r.ok ? 'Round-trip OK' : 'Round-trip MISMATCH — do not trust this run') + '</h2>' +
      '<p>Rows: ' + r.n.toLocaleString() + ' (CSV parsed: ' + r.csvCount.toLocaleString() + ')</p>' +
      '<p>CSV string parse: ' + r.csvMs.toFixed(1) + ' ms</p>' +
      '<p>Binary ArrayBuffer round-trip: ' + r.binMs.toFixed(1) + ' ms</p>' +
      '<p><strong>Speedup: ' + r.speedup.toFixed(2) + 'x</strong> (binary vs CSV, in this browser, on this device)</p>' +
      '<p>First value: ' + r.first.join(', ') + ' | Last value: ' + r.last.join(', ') + '</p></div>' +
      '<p class="privacy">Browser version measures CSV vs binary in your browser; the Python Arrow + mmap version is in the repo (shmpipe/) and measured 6.6x at 5M rows. Your number will differ by device and browser — that is the point of running it live.</p>');
  }, 30);
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {scanSecrets: scanSecrets, diffFunctions: diffFunctions, parseCSV: parseCSV, csvStats: csvStats, sha256Hex: sha256Hex, traceCSV: traceCSV, parseCarbonForecast: parseCarbonForecast, wattShift: wattShift, shmBenchmark: shmBenchmark, parseInputs: parseInputs};
}
