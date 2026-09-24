/* The Reading Room — shared helpers. Authority C.
   The build concatenates app/*.js in name order inside one function scope. */
var D = window.DATA, H = window.HEL;
H.init(D.inventory, D.register, D.common);

var REG = {};
D.register.forEach(function (u) { REG[u.form] = u; });
var BYREF = {};
D.entries.forEach(function (e) { BYREF[key(e)] = e; });
var FEAT = D.featured || {};
var LOCI = D.locus_names || {};

function key(e) { return e.cid + (e.part ? "/" + e.part : ""); }
function $(s, r) { return (r || document).querySelector(s); }
function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
  });
}
function el(tag, cls, html) {
  var x = document.createElement(tag);
  if (cls) x.className = cls;
  if (html != null) x.innerHTML = html;
  return x;
}
function fmt(n) { return Number(n).toLocaleString("en-US"); }
function pct(x, d) { return (x * 100).toFixed(d == null ? 1 : d) + "%"; }
function parse(text) { try { return H.parseSegment(text); } catch (e) { return null; } }
function plural(n, one, many) { return fmt(n) + " " + (n === 1 ? one : (many || one + "s")); }

/* per-viewer conveniences only; the page renders the same without them */
var store = {
  get: function (k, d) {
    try { var v = window.localStorage.getItem("reading-room:" + k); return v === null ? d : JSON.parse(v); }
    catch (e) { return d; }
  },
  set: function (k, v) {
    try { window.localStorage.setItem("reading-room:" + k, JSON.stringify(v)); } catch (e) { /* storage refused */ }
  }
};

/* inline markup for a unit: roots link to their register entry */
function unitLink(form) {
  var u = REG[form];
  if (!u) return '<span class="u">' + esc(form) + "</span>";
  return '<button class="u reg" data-unit="' + esc(form) + '" title="' + esc(u.cid + (u.gloss ? " — " + u.gloss + "?" : "")) + '">' + esc(form) + "</button>";
}

function sevClass(sev) { return sev === "ill-formed" ? "ill-formed" : sev === "damaged" ? "damaged" : "note"; }
function findingChips(list) {
  var shown = list.filter(function (f) { return f.severity !== "note"; });
  if (!shown.length) return '<div class="findings"><span class="fnd ok">well-formed · no damage recorded</span></div>';
  return '<div class="findings">' + shown.map(function (f) {
    return '<span class="fnd ' + sevClass(f.severity) + '" title="' + esc(f.where) + '">' + esc(f.code) + " · " + esc(f.where) + " · " + esc(f.message) + "</span>";
  }).join("") + "</div>";
}

/* the interlinear gloss (A §6.3): catalog-form roots, G3 formatives queried */
function glossHTML(seg) {
  return '<div class="gloss">' + H.gloss(seg).map(function (c) {
    return '<div><span class="t">' + esc(c[0]) + '</span><span class="g">' + esc(c[1]) + "</span></div>";
  }).join("") + "</div>";
}

function readbackHTML(seg) {
  var rb = H.readback(seg);
  return '<div class="turns"><div><b>A</b><span>' + esc(rb[0]) + '</span></div><div><b>B</b><span>' + esc(rb[1]) +
    '</span></div><div><b>A</b><span>' + esc(rb[2]) + "</span></div></div>";
}

function translationHTML(seg) {
  var t = H.translate(seg);
  var out = '<p class="tr">“' + esc(t.text) + '”</p>';
  if (t.residue.length) out += '<div class="residue">' + t.residue.map(function (r) { return "<span>" + esc(r) + "</span>"; }).join("") + "</div>";
  return out;
}

/* pronunciation, with a remembered tradition */
var TRAD = store.get("trad", "standard");
var TRAD_LABEL = { standard: "1949 Standard", chicago: "Chicago Reading Room", second: "Second branch" };
function pronounce(seg, trad) {
  if (trad === "second") return H.recite(seg, "second");
  return H.ipa(seg, trad);
}
function pronHTML(seg, id) {
  var t = '<div class="toggle" role="group" aria-label="Pronunciation tradition">' + ["standard", "chicago", "second"].map(function (k) {
    return '<button data-trad="' + k + '" aria-pressed="' + (k === TRAD ? "true" : "false") + '">' + TRAD_LABEL[k] + "</button>";
  }).join("") + "</div>";
  return '<div class="pron" data-seg="' + esc(id) + '">' + t + '<div class="ipa">' + esc(pronounce(seg, TRAD)) + "</div></div>";
}
var PRON_SEGS = {};
document.addEventListener("click", function (ev) {
  var b = ev.target.closest && ev.target.closest("[data-trad]");
  if (!b) return;
  TRAD = b.getAttribute("data-trad");
  store.set("trad", TRAD);
  $$(".pron").forEach(function (p) {
    var seg = PRON_SEGS[p.getAttribute("data-seg")];
    if (!seg) return;
    $$("[data-trad]", p).forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-trad") === TRAD ? "true" : "false"); });
    $(".ipa", p).textContent = pronounce(seg, TRAD);
  });
});
var segSerial = 0;
function registerSeg(seg) { var id = "s" + (++segSerial); PRON_SEGS[id] = seg; return id; }

/* views */
var VIEWS = ["catalogue", "bench", "recitation", "field", "figures", "findings", "chronology"];
var RENDER = {}, rendered = {};
function show(v) {
  if (VIEWS.indexOf(v) < 0) v = "catalogue";
  $$("#tabs button").forEach(function (b) { b.setAttribute("aria-selected", b.getAttribute("data-v") === v ? "true" : "false"); });
  $$("main > section").forEach(function (s) { s.hidden = s.getAttribute("data-view") !== v; });
  if (!rendered[v] && RENDER[v]) { RENDER[v](); rendered[v] = true; }
  store.set("tab", v);
}
