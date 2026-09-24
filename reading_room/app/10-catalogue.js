/* Catalogue: the drawer, its filters, and the card for one accession. */
var CHANNELS = ["Ch-1", "Ch-2", "Ch-3", "Ch-4"], STRATA = ["I", "II", "III", "IV"];
var CH_NAME = { "Ch-1": "incised object", "Ch-2": "plate or hand copy", "Ch-3": "instrument log", "Ch-4": "recitation" };
function tx(e) {
  if (e._tx != null) return e._tx;
  e._tx = e.segments.length ? e.segments.map(function (s) { return s.translit; }).join(" | ") : e.units.join(" ");
  return e._tx;
}
function isIII(e) { return /^III/.test(e.stratum); }
var FILTERS = [
  { k: "featured", label: "Start here", test: function (e) { return !!FEAT[key(e)]; } },
  { k: "named", label: "Named", test: function (e) { return !!e.field_name; } },
  { k: "damaged", label: "Damaged", test: function (e) { return /worn|fractured|eroded/.test(e.condition); } },
  { k: "pairs", label: "Bound pairs", test: function (e) { return /(^|[ ·-])kalsira-ru(?![-\w])|lartuki(-in)?-halu/.test(tx(e)); } },
  { k: "stack", label: "Stacked warrants", test: function (e) { return /(lekur hos|hos lekur)/.test(tx(e)); } },
  { k: "auth", label: "AUTH grade", test: function (e) { return /-lan(?=[-\s=·|]|$)/.test(tx(e)); } },
  { k: "41", label: "[41]", test: function (e) { return tx(e).indexOf("[41]") >= 0; } }
];
var CAT = { ch: null, st: null, f: {}, q: "", sel: null };

/* Stratum III index: which sequences each unit occurs in */
var III_INDEX = {};
D.entries.forEach(function (e) {
  if (!isIII(e)) return;
  e.units.forEach(function (u) { (III_INDEX[u] = III_INDEX[u] || {})[key(e)] = 1; });
});

function chipRow(host, items, get, set) {
  host.innerHTML = "";
  items.forEach(function (it) {
    var b = el("button", "chip", esc(it.label));
    b.setAttribute("aria-pressed", get(it) ? "true" : "false");
    b.addEventListener("click", function () { set(it); renderChips(); renderList(); });
    host.appendChild(b);
  });
}
function renderChips() {
  chipRow($("#chan"), [{ v: null, label: "All channels" }].concat(CHANNELS.map(function (c) { return { v: c, label: c }; })),
    function (it) { return CAT.ch === it.v; }, function (it) { CAT.ch = it.v; });
  chipRow($("#strat"), [{ v: null, label: "All strata" }].concat(STRATA.map(function (s) { return { v: s, label: "Stratum " + s }; })),
    function (it) { return CAT.st === it.v; }, function (it) { CAT.st = it.v; });
  chipRow($("#feat"), FILTERS, function (it) { return !!CAT.f[it.k]; }, function (it) { CAT.f[it.k] = !CAT.f[it.k]; });
}
function haystack(e) {
  if (e._hay) return e._hay;
  e._hay = [e.ref, e.field_name, e.locus, LOCI[e.locus], e.accession_year, e.catalogued_year, e.channel, CH_NAME[e.channel],
    "stratum " + e.stratum, e.source, e.condition, tx(e)].filter(Boolean).join(" ").toLowerCase();
  return e._hay;
}
function matches(e) {
  if (CAT.ch && e.channel !== CAT.ch) return false;
  if (CAT.st && e.stratum.split(" ")[0] !== CAT.st) return false;
  for (var i = 0; i < FILTERS.length; i++) if (CAT.f[FILTERS[i].k] && !FILTERS[i].test(e)) return false;
  if (CAT.q) {
    var h = haystack(e), terms = CAT.q.toLowerCase().split(/\s+/).filter(Boolean);
    for (var j = 0; j < terms.length; j++) if (h.indexOf(terms[j]) < 0) return false;
  }
  return true;
}
var ROWS = null;
function buildRows() {
  var list = $("#list");
  ROWS = D.entries.map(function (e) {
    var b = el("button", "row");
    b.setAttribute("data-k", key(e));
    b.innerHTML = '<span class="num">' + esc(e.ref) + '</span><span class="meta">' + esc(e.channel + " · " + e.stratum.replace(" (provisional)", "p") +
      (e.accession_year ? " · " + e.accession_year : "") + (e.locus ? " · " + e.locus : "")) + "</span>" +
      (e.field_name ? '<span class="fn">' + esc(e.field_name) + "</span>" : "") +
      '<span class="tx">' + esc(tx(e)) + "</span>";
    b.addEventListener("click", function () { select(key(e), true); });
    list.appendChild(b);
    return { e: e, b: b };
  });
}
function renderList() {
  var n = 0;
  ROWS.forEach(function (r) { var ok = matches(r.e); r.b.hidden = !ok; if (ok) n++; });
  $("#count").textContent = n === D.entries.length ? plural(n, "accession") + " · catalogue order (1949 accession numbering)"
    : fmt(n) + " of " + plural(D.entries.length, "accession") + " shown";
}

function badge(text, cls) { return '<span class="badge' + (cls ? " " + cls : "") + '">' + esc(text) + "</span>"; }

function select(k, fromList) {
  var e = BYREF[k];
  if (!e) return;
  CAT.sel = k;
  store.set("sel", k);
  ROWS.forEach(function (r) { r.b.setAttribute("aria-current", key(r.e) === k ? "true" : "false"); });
  renderCard(e);
  if (fromList && window.matchMedia && window.matchMedia("(max-width: 860px)").matches) {
    var c = $("#card"); if (c.scrollIntoView) c.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function renderCard(e) {
  var c = $("#card"), html = [];
  PRON_SEGS = {};
  html.push('<div class="card-head"><h2>' + esc(e.ref) + "</h2>" + (e.field_name ? '<span class="fname">' + esc(e.field_name) + "</span>" : "") + "</div>");
  var b = [badge(e.channel + " · " + e.source)];
  b.push(badge("Stratum " + e.stratum, isIII(e) ? "s3" : ""));
  if (e.locus) b.push(badge(e.locus + (LOCI[e.locus] ? " · " + LOCI[e.locus] : "")));
  if (e.accession_year) b.push(badge("accessioned " + e.accession_year));
  b.push(badge("catalogued " + e.catalogued_year));
  if (e.condition !== "intact") b.push(badge(e.condition, e.condition === "transmitted" ? "" : "dmg"));
  html.push('<div class="badges">' + b.join("") + "</div>");
  var f = FEAT[key(e)];
  if (f) html.push('<div class="note"><h3>' + esc(f.title) + "</h3>" + f.body.map(function (p) { return "<p>" + p + "</p>"; }).join("") + "</div>");
  c.innerHTML = html.join("");
  if (isIII(e)) renderIII(c, e);
  else if (e.channel === "Ch-3") renderLog(c, e);
  else e.segments.forEach(function (s, i) { renderSegment(c, e, s, i); });
  renderRegisterNotes(c, e);
  renderUnits(c, e);
  var links = [];
  if (!e.part && BYREF[e.cid + "/III"]) links.push('<button class="btn alt" data-go="' + e.cid + '/III">Open the Stratum III field on this object</button>');
  if (e.part === "III") links.push('<button class="btn alt" data-go="' + e.cid + '">Open the host record, ' + esc(e.cid) + "</button>");
  var sow = D.entries.filter(function (x) { return x.field_name === "the Sowerby recitation"; })[0];
  if (sow && e.cid === "CSC-1146") links.push('<button class="btn alt" data-go="' + key(sow) + '">Open the Sowerby recitation, ' + esc(sow.ref) + "</button>");
  if (sow && e.cid === sow.cid) links.push('<button class="btn alt" data-go="CSC-1146">Open the object, CSC-1146</button>');
  if (links.length) c.appendChild(el("div", "btns", links.join("")));
}

function layer(label, inner) {
  return '<div class="layer"><div class="label">' + label + "</div>" + inner + "</div>";
}

function renderSegment(c, e, s, i) {
  var seg = parse(s.translit), box = el("div", "segblock");
  if (!seg) { box.innerHTML = '<p class="err">Could not parse ' + esc(s.translit) + "</p>"; c.appendChild(box); return; }
  var id = registerSeg(seg), out = [];
  if (e.segments.length > 1) out.push('<div class="label segn">Segment ' + (i + 1) + " of " + e.segments.length + "</div>");
  if (e.channel === "Ch-4") {
    out.push(layer("1 · Trace", '<p class="intro">Ch-4 has no trace. It exists only as recitation; the line below is the Archive’s back-transliteration into written convention, which is itself an analytic act and is contested (A §8, Example 3).</p>'));
  } else {
    var what = e.source === "hand copy" ? "as the copyist drew it · Ch-2 hand copy" : e.source === "plate" ? "photographic plate · Ch-2" : "incised · Ch-1";
    out.push(layer("1 · Trace <b>· " + what + "</b>", '<div class="trace">' + H.traceSVG(seg, { label: "Trace of " + e.ref }) + "</div>"));
  }
  out.push(layer("2 · Transliteration <b>· the 1908 Standard, as reformed 1988</b>", '<div class="translit">' + esc(s.translit) + "</div>"));
  out.push(layer("3 · Field pronunciation", pronHTML(seg, id)));
  out.push(layer("4 · Gloss <b>· catalog-form roots; G3 formatives queried</b>", glossHTML(seg)));
  if (seg.words.length && e.channel !== "Ch-4") out.push(layer("Readback <b>· A §6.2</b>", readbackHTML(seg)));
  out.push(layer("Operational English <b>· with its residue</b>", translationHTML(seg)));
  var checks = H.check(seg, e.channel);
  var prof = H.profile(seg);
  out.push(layer("Findings <b>· profile " + prof + (prof === "I/II" ? " (either stratum)" : "") + " · catalogued Stratum " + esc(e.stratum) + "</b>", findingChips(checks)));
  var complete = H.edges(seg).filter(function (x) { return x.kind === "complete"; }).length;
  var btns = '<button class="btn" data-bench="' + esc(s.translit) + '">Open in the workbench</button>';
  if (complete) btns += '<button class="btn alt" data-bench="' + esc(s.translit) + '" data-rev="' + (complete - 1) + '">Reverse the last edge</button>';
  out.push('<div class="btns">' + btns + "</div>");
  box.innerHTML = out.join("");
  c.appendChild(box);
}

function renderLog(c, e) {
  var box = el("div", "segblock");
  box.innerHTML = layer("1 · Trace", '<p class="intro">Ch-3 is instrument output: the sequence of units is recoverable and the shape is not. Stratum IV is a log, not a sentence; it is read as a tape (A §7.3).</p>') +
    layer("Log tape", '<div class="trace log">' + H.logSVG(e.units) + "</div>") +
    layer("2 · Transliteration", '<div class="translit">' + e.units.map(esc).join(" ") + "</div>") +
    layer("Tokens", '<p class="intro">' + plural(e.units.length, "unit") + ". Units shared with the functional register: " +
      fmt(e.units.filter(function (u) { return REG[u] || H.isTranslit(u) && D.inventory.slots.warrant[u]; }).length) + ".</p>");
  c.appendChild(box);
}

function iiiFacts(e) {
  var u = e.units, types = [], pos = {};
  u.forEach(function (x, i) { if (!pos[x]) { pos[x] = []; types.push(x); } pos[x].push(i + 1); });
  var same = function (k) { var o = BYREF[k]; return o && o.units.join(" ") === u.join(" "); };
  var hapax = types.filter(function (t) { return Object.keys(III_INDEX[t] || {}).filter(function (k) { return k !== key(e) && !same(k); }).length === 0; });
  var coda = u.filter(function (x) { var s = H.syllables(x) || [x]; return !/[aeiou]$/.test(s[s.length - 1]); }).length;
  var syl = u.reduce(function (n, x) { return n + (H.syllables(x) || [x]).length; }, 0);
  var ambiguous = types.filter(function (t) { return H.segment(t).length > 1; });
  var assignable = types.filter(function (t) { return REG[t] && REG[t].kind === "root"; });
  var rec = types.filter(function (t) { return pos[t].length > 1; });
  var rows = [
    ["Tokens", u.length + (u.length % 3 === 0 ? " · divisible by three" : " · not divisible by three")],
    ["Types", types.length],
    ["Recurring inside the record", rec.length ? rec.map(function (t) { return t + " ×" + pos[t].length + " at " + pos[t].join(", "); }).join("; ") : "none"],
    ["Types in no other sequence", hapax.length + " of " + types.length + (types.length > hapax.length ? " (" + types.filter(function (t) { return hapax.indexOf(t) < 0; }).join(", ") + " recur elsewhere)" : "")],
    ["Tokens ending in a coda", coda + " of " + u.length],
    ["Mean syllables per unit", (syl / u.length).toFixed(1)],
    ["Admitting two legal segmentations", ambiguous.length ? ambiguous.map(function (t) { return t + " (" + H.segment(t).map(function (s) { return s.join("-"); }).join(" or ") + ")"; }).join("; ") : "none"],
    ["Assignable units (Condition 1)", assignable.length || "0"]
  ];
  return '<div class="kv">' + rows.map(function (r) { return "<span>" + esc(r[0]) + "</span><span>" + esc(r[1]) + "</span>"; }).join("") + "</div>";
}

function renderIII(c, e) {
  var box = el("div", "segblock"), u = e.units, lines = [];
  for (var i = 0; i < u.length; i += 3) lines.push(u.slice(i, i + 3).join(" · "));
  var std = H.ipa({ words: [], warrants: [], free: u }, "standard"), chi = H.ipa({ words: [], warrants: [], free: u }, "chicago");
  var out = [];
  var where = e.iii_position === "after completed segment" ? "after the host record’s last completed segment" :
    e.iii_position === "recitation" ? "a recitation; no object" : e.iii_position === "whole record" ? "the whole of the record" : "on an object that bears no trace line";
  if (e.channel === "Ch-4") out.push(layer("1 · Field", '<p class="intro">A recitation. There is nothing to draw.</p>'));
  else out.push(layer("1 · Field <b>· " + esc(where) + "</b>", '<div class="trace field">' + H.fieldSVG(u) + "</div>"));
  out.push(layer("2 · Transliteration", '<div class="translit">' + lines.map(esc).join("<br>") + "</div>"));
  out.push(layer("3 · Field pronunciation <b>· stress final, no reduction, ever</b>", '<div class="ipa">1949 Standard ' + esc(std) + '</div><div class="ipa">Chicago ' + esc(chi) + "</div>"));
  out.push(layer("4 · Gloss", '<div class="refusal"><span>Gloss</span><span class="empty">(none — Stratum III)</span><span>Grade</span><span class="empty">(none — the grade system grades readings; there is no reading)</span><span>Translation</span><span class="empty">(none)</span><span>Class</span><span>' + esc(e.stratum) + (e.stratum === "III (provisional)" ? " — six to eight units" : " — all three conditions") + "</span></div>"));
  out.push(layer("What the catalogue can state <b>· computed from the corpus on this page</b>", iiiFacts(e)));
  out.push('<p class="intro">A damaged segment is a sentence with a hole in it. A Stratum III sequence is not a sentence and has no hole (A-reserve §2.2).</p>');
  box.innerHTML = out.join("");
  c.appendChild(box);
}

function renderRegisterNotes(c, e) {
  var notes = [];
  (e.notes || []).forEach(function (n) { notes.push(esc(n)); });
  var r = e.register || {};
  (r.stratum_II_environments || []).forEach(function (x) {
    notes.push("Stratum II environment (A §7.1): the committee cut the head half before the vowel-initial root <b>" + esc(x.root) + "</b>; the trace there is " +
      (x.trace === "short" ? "short — the notch count is too low for a head" : "indeterminate") +
      (x.older_branch_cut ? "; the older branch register " + (x.older_branch_cut === "present" ? "already shows the cut" : "does not show the cut") : "") + ".");
  });
  (r.copy_variants || []).forEach(function (v) {
    notes.push("Copy variant in the branch register: <b>" + esc(v[0]) + "</b> copied as <b>" + esc(v[1]) + "</b> — the /h/–/k/ pair the code cannot tell apart (A §6.1b).");
  });
  if (r.page_break_marked) notes.push("A page ends inside this copy: the copyist’s <b>-ar</b> at the break is marked in the register (the Hallam dispute, A §4.6b).");
  if (!notes.length) return;
  c.appendChild(el("div", "note", "<h3>Register</h3>" + notes.map(function (n) { return "<p>" + n + "</p>"; }).join("")));
}

function renderUnits(c, e) {
  var seen = {}, units = [];
  function add(f) { if (f && REG[f] && !seen[f]) { seen[f] = 1; units.push(REG[f]); } }
  e.segments.forEach(function (s) {
    var seg = parse(s.translit); if (!seg) return;
    seg.words.forEach(function (w) { add(w.root); if (w.coord) add(w.coord.locus); });
    seg.free.forEach(add);
  });
  if (!units.length) return;
  var rows = units.map(function (u) {
    var r = (u.readings || []).map(function (x) { return "<i>" + esc(x[0]) + ":</i> " + esc(x[1]); }).join(" · ");
    return "<div><b>" + esc(u.form) + "</b><span>" + esc(u.cid) + " · " + (u.gloss ? "“" + esc(u.gloss) + "?”" : "no gloss") + " · " + esc(u.grade) +
      (u.commanded ? " · commanded core" : "") + (u.kind === "ritual" ? " · Ch-4 only, not translated" : "") +
      (r ? "<br>" + r : "") + (u.note ? "<br><span class=\"quiet\">" + esc(u.note) + "</span>" : "") + "</span></div>";
  });
  c.appendChild(el("div", "layer", '<div class="label">Units on this record <b>· the unit register</b></div><div class="readings">' + rows.join("") + "</div>"));
}

document.addEventListener("click", function (ev) {
  var g = ev.target.closest && ev.target.closest("[data-go]");
  if (g) { show("catalogue"); select(g.getAttribute("data-go"), true); }
});

RENDER.catalogue = function () {
  renderChips();
  buildRows();
  var q = $("#q");
  q.addEventListener("input", function () { CAT.q = q.value.trim(); renderList(); });
  renderList();
};
