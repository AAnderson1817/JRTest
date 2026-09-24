/* Workbench: type a segment, get every layer and every finding, live. */
var SAMPLES = [
  ["Example 1", "harnuli-in-ken · ke-telnuro-is-ru · ru-kalsira-in=hilun-to-pukal · tir lekur"],
  ["the Ladder", "harnuli-ar-pel-sen · pe-kurhali-in=hilun-nu-hilun · hos"],
  ["the custodial attestation", "sarkile-in-sil · si-lartuki-ol=hilun-sa-kihar · lunkani · [41]"],
  ["the waiting", "kanirlu-in-ru-nir-kur · ru-yuntiha-in=hilun-to-kihar · tuwalsi · [41]"],
  ["a fracture", "ketirnu-in-tul-lan-lar-lun"],
  ["a worn cartouche", "pe-olsihe-in=-nu-hilun · hos"],
  ["ill-formed", "rukalti-in-ru-ka-lar · ru-siltoni-in · tir"],
  ["the long word", "harnuli-in-ru-lan-lun · ru-lankiro-in=hilun-to-hilun · rosilpe · [41]"],
  ["CSC-1146", "walnisen pehisar tirakur pekalar munlisen tirakur walnisen nusar tirakur"]
];

var FORMS = {};
(function () {
  var I = D.inventory;
  Object.keys(I.edge_classes).forEach(function (c) { FORMS[I.edge_classes[c].tail] = "tail"; FORMS[I.edge_classes[c].head] = "head"; });
  ["incidence", "grade", "unent", "discharge", "polarity", "rscope", "scope", "pass", "phase", "warrant"].forEach(function (s) {
    Object.keys(I.slots[s]).forEach(function (f) { FORMS[f] = s; });
  });
  FORMS.hilun = "gap";
})();

function syllableCount(seg) {
  var n = 0;
  function add(f) { if (f && f !== "[41]") n += (H.syllables(f) || [f]).length; }
  H.tokens(seg).forEach(add);
  return n;
}

function looksIII(t) {
  if (/[·=\-\[]/.test(t)) return null;
  var u = t.trim().split(/\s+/).filter(Boolean);
  if (u.length < 2) return null;
  for (var i = 0; i < u.length; i++) if (!H.isTranslit(u[i])) return null;
  return u;
}

function benchIII(out, units) {
  var assigned = units.filter(function (u) { return (REG[u] && REG[u].kind === "root") || FORMS[u]; });
  var cls, why;
  if (assigned.length) { cls = "not Stratum III"; why = "Condition 1 fails: " + plural(assigned.length, "assignable unit") + " (" + assigned.join(", ") + ")."; }
  else if (units.length < 6) { cls = "unassigned, short"; why = "Condition 3: fewer than six units."; }
  else if (units.length < 9) { cls = "III (provisional)"; why = "Six to eight units."; }
  else { cls = "III"; why = "Condition 1 holds: no unit is a formative, a filler, a warrant or a registered root, and none segments as a node word on a registered root. Conditions 2(a)–(c) are about an object’s field and its channel, and a workbench has neither."; }
  out.push('<div class="status"><span class="fnd ' + (assigned.length ? "ill-formed" : "ok") + '">' + esc(cls) + "</span> " + esc(why) + "</div>");
  out.push(layer("Field", '<div class="trace field">' + H.fieldSVG(units) + "</div>"));
  out.push(layer("Gloss", '<div class="refusal"><span>Gloss</span><span class="empty">(none)</span><span>Grade</span><span class="empty">(none)</span></div>'));
  out.push(layer("What can be stated", iiiFacts({ cid: "workbench", part: "", units: units })));
}

function renderBench() {
  var host = $("#bench"), ta = $("#bench-in"), out = [], text = ta.value.trim();
  var res = $("#bench-out");
  PRON_SEGS = {};
  if (!text) { res.innerHTML = '<p class="intro">Type a segment above, or pick a sample.</p>'; return; }
  var units = looksIII(text);
  if (units) { benchIII(out, units); res.innerHTML = out.join(""); return; }
  var seg;
  try { seg = H.parseSegment(text); }
  catch (e) { res.innerHTML = '<p class="err">' + esc(e.message || String(e)) + "</p>" + '<p class="intro">Node words are separated by <code>·</code> (or <code>*</code>); morphemes by <code>-</code>; a coordinate follows <code>=</code> as LOCUS-PASS-PHASE, and an empty slot is lost, not <code>hilun</code>.</p>'; return; }
  if (!seg.words.length && !seg.free.length) { res.innerHTML = '<p class="err">A warrant needs a record to warrant.</p>'; return; }
  var checks = H.check(seg, "Ch-1"), ill = checks.some(function (f) { return f.severity === "ill-formed"; }),
    dmg = checks.some(function (f) { return f.severity === "damaged"; });
  var state = ill ? '<span class="fnd ill-formed">ill-formed</span>' : dmg ? '<span class="fnd damaged">well-formed, damaged</span>' : '<span class="fnd ok">well-formed</span>';
  out.push('<div class="status">' + state + " profile " + esc(H.profile(seg)) + " · " + plural(H.tokens(seg).length, "token") + " · " + plural(syllableCount(seg), "syllable") + "</div>");
  if (seg.words.some(function (w) { return w.grade === "lan"; }))
    out.push('<div class="warnbar">AUTH grade. HEL cannot determine whether AUTH is performative, so Archive Field Protocol restricts speaking AUTH forms aloud within a defined distance of an active locus (A §4.3). The protocol asserts nothing; it is a precaution taken under ignorance. You are in the Reading Room.</div>');
  if (ill || dmg) out.push(layer("Findings", findingChips(checks)));
  out.push(layer("Trace", '<div class="trace">' + H.traceSVG(seg, { label: "Trace of the workbench segment" }) + "</div>"));
  out.push(layer("Transliteration <b>· normalised</b>", '<div class="translit">' + esc(H.translit(seg)) + "</div>"));
  out.push(layer("Gloss", glossHTML(seg)));
  if (seg.words.length) out.push(layer("Readback", readbackHTML(seg)));
  out.push(layer("Operational English", translationHTML(seg)));
  out.push(layer("Field pronunciation", pronHTML(seg, registerSeg(seg))));
  var complete = H.edges(seg).filter(function (x) { return x.kind === "complete"; });
  if (complete.length) {
    out.push(layer("Reverse an edge <b>· the anchor rule (A §5.2a)</b>", '<div class="btns">' + complete.map(function (x, i) {
      return '<button class="btn alt" data-rev-now="' + i + '">' + esc(seg.words[x.origin].root + " → " + seg.words[x.dest].root + " (" + x.cls + ")") + "</button>";
    }).join("") + '</div><p class="intro">Reversing an edge moves its tail to the other word. When that word carries the coordinate, carrier and anchor collapse into one word and the coordinate stops composing: E-ANCHOR. The record is reversible; the network is not.</p>'));
  }
  res.innerHTML = out.join("");
}

function palette() {
  var I = D.inventory, groups = [];
  groups.push(["Edge classes (tail · head)", Object.keys(I.edge_classes).map(function (c) {
    var e = I.edge_classes[c];
    return '<button class="chip" data-ins="-' + e.tail + '" title="' + esc(c + " tail, " + e.grade) + '">-' + e.tail + "</button>" +
      '<button class="chip" data-ins="' + e.head + '-" title="' + esc(c + " head, " + e.grade) + '">' + e.head + "- <i>" + c + "</i></button>";
  }).join("")]);
  ["incidence", "grade", "unent", "discharge", "polarity", "rscope", "scope"].forEach(function (s) {
    groups.push([s, Object.keys(I.slots[s]).map(function (f) {
      var x = I.slots[s][f];
      return '<button class="chip" data-ins="-' + f + '" title="' + esc(x.abbr + " — " + x.meaning + " (" + x.grade + ")") + '">-' + f + " <i>" + esc(x.abbr) + "</i></button>";
    }).join("")]);
  });
  groups.push(["coordinate", '<button class="chip" data-ins="=hilun-sa-kihar">=LOCUS-PASS-PHASE</button>' +
    Object.keys(I.slots.pass).concat(Object.keys(I.slots.phase), ["hilun"]).map(function (f) {
      var x = I.slots.pass[f] || I.slots.phase[f] || { abbr: "GAP", meaning: "unfilled, and the record says so" };
      return '<button class="chip" data-ins="' + f + '" title="' + esc(x.abbr + " — " + x.meaning) + '">' + f + " <i>" + esc(x.abbr) + "</i></button>";
    }).join("")]);
  groups.push(["warrants", Object.keys(I.slots.warrant).map(function (f) {
    var x = I.slots.warrant[f];
    return '<button class="chip" data-ins=" · ' + f + '" title="' + esc(x.meaning) + '">' + esc(f) + " <i>" + esc(x.abbr) + "</i></button>";
  }).join("")]);
  groups.push(["commanded core roots", D.register.filter(function (u) { return u.commanded; }).map(function (u) {
    return '<button class="chip" data-ins="' + u.form + '" title="' + esc(u.cid + (u.gloss ? " — " + u.gloss + "?" : "")) + '">' + u.form + "</button>";
  }).join("")]);
  return '<details class="palette"><summary>Formatives and roots — click to insert</summary>' + groups.map(function (g) {
    return '<div class="pal"><div class="label">' + esc(g[0]) + '</div><div class="chips">' + g[1] + "</div></div>";
  }).join("") + "</details>";
}

RENDER.bench = function () {
  var host = $("#bench");
  host.innerHTML = '<div class="section"><h2>Workbench</h2><p class="intro">The same engine that built the catalogue, running in this page. Write a segment in transliteration and every layer is derived from it: the trace, the gloss, the radio readback, the Archive’s operational English with its residue, and three pronunciations. Nothing here consults a meaning; the engine checks form, and form is all the Archive has.</p></div>' +
    '<textarea id="bench-in" spellcheck="false" aria-label="Segment in transliteration"></textarea>' +
    '<div class="btns" id="bench-samples">' + SAMPLES.map(function (s, i) { return '<button class="btn" data-sample="' + i + '">' + esc(s[0]) + "</button>"; }).join("") + "</div>" +
    palette() + '<div class="bench-out" id="bench-out"></div>';
  var ta = $("#bench-in");
  ta.value = store.get("bench", SAMPLES[0][1]);
  var t = null;
  ta.addEventListener("input", function () { clearTimeout(t); t = setTimeout(function () { store.set("bench", ta.value); renderBench(); }, 120); });
  host.addEventListener("click", function (ev) {
    var s = ev.target.closest("[data-sample]");
    if (s) { ta.value = SAMPLES[+s.getAttribute("data-sample")][1]; store.set("bench", ta.value); renderBench(); return; }
    var ins = ev.target.closest("[data-ins]");
    if (ins) {
      var v = ins.getAttribute("data-ins"), a = ta.selectionStart || ta.value.length, b = ta.selectionEnd || a;
      ta.value = ta.value.slice(0, a) + v + ta.value.slice(b);
      ta.focus(); ta.selectionStart = ta.selectionEnd = a + v.length;
      store.set("bench", ta.value); renderBench(); return;
    }
    var r = ev.target.closest("[data-rev-now]");
    if (r) {
      var seg = parse(ta.value.trim()); if (!seg) return;
      var rev = H.reverse(seg, +r.getAttribute("data-rev-now"));
      if (rev) { ta.value = H.translit(rev); store.set("bench", ta.value); renderBench(); }
    }
  });
  renderBench();
};

/* "Open in the workbench" from a catalogue card */
document.addEventListener("click", function (ev) {
  var b = ev.target.closest && ev.target.closest("[data-bench]");
  if (!b) return;
  var text = b.getAttribute("data-bench"), rev = b.getAttribute("data-rev");
  if (rev != null) { var seg = parse(text), r = seg && H.reverse(seg, +rev); if (r) text = H.translit(r); }
  store.set("bench", text);
  show("bench");
  $("#bench-in").value = text;
  renderBench();
  var top = $("#tabs"); if (top.scrollIntoView) top.scrollIntoView({ block: "start" });
});
