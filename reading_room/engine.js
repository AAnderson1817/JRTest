/* HEL engine (browser + Node). Authority C.
 * A port of hel/parse.py and hel/grammar.py sufficient to parse, check, gloss, read
 * back and pronounce any segment, plus the trace renderer (the script concept of
 * A §9 with the Phase 1 condition: a distinct silhouette per edge class and a fixed
 * cartouche outer form). Nothing sealed is loaded here, ever.
 */
(function (root) {
  "use strict";
  var HEL = {};
  var INV = null, REG = {}, HEADS = {}, TAILS = {}, SUFFIX = {}, ORDER = {}, WARRANTS = {},
      PASSV = {}, PHASEV = {}, RITUAL = {}, SANCT = [], OPEN = {}, CLOSED = {}, ONSET0 = {}, COMMON = {}, SECOND_IRR = {};
  var GAP = "hilun";

  HEL.init = function (inventory, register, common) {
    INV = inventory;
    REG = {}; RITUAL = {};
    (register || []).forEach(function (u) { REG[u.form] = u; if (u.kind === "ritual") RITUAL[u.form] = u; });
    HEADS = {}; TAILS = {};
    Object.keys(INV.edge_classes).forEach(function (c) {
      var e = INV.edge_classes[c];
      TAILS[e.tail] = c; HEADS[e.head] = c;
    });
    SUFFIX = {};
    ["incidence", "grade", "unent", "discharge", "polarity", "rscope", "scope"].forEach(function (slot) {
      Object.keys(INV.slots[slot]).forEach(function (f) { SUFFIX[f] = slot; });
    });
    Object.keys(TAILS).forEach(function (f) { SUFFIX[f] = "tail"; });
    INV.suffix_order.forEach(function (s, i) { ORDER[s] = i; });
    WARRANTS = INV.slots.warrant; PASSV = INV.slots.pass; PHASEV = INV.slots.phase;
    SANCT = INV.sanctioned.open.concat(INV.sanctioned.closed, INV.sanctioned.onsetless);
    OPEN = {}; CLOSED = {}; ONSET0 = {};
    INV.sanctioned.open.forEach(function (s) { OPEN[s] = 1; });
    INV.sanctioned.closed.forEach(function (s) { CLOSED[s] = 1; });
    INV.sanctioned.onsetless.forEach(function (s) { ONSET0[s] = 1; });
    COMMON = (common && common.common) || common || {};
    SECOND_IRR = (common && common.second_irregular) || {};
  };

  /* ---------------------------------------------------------------- phonology */
  var segCache = {};
  function segment(word) {
    if (word in segCache) return segCache[word];
    if (!word) return [[]];
    var out = [];
    for (var i = 0; i < SANCT.length; i++) {
      var s = SANCT[i];
      if (word.indexOf(s) === 0) {
        var rest = segment(word.slice(s.length));
        for (var j = 0; j < rest.length; j++) out.push([s].concat(rest[j]));
      }
    }
    segCache[word] = out;
    return out;
  }
  function syllables(word) {
    var segs = segment(word);
    if (!segs.length) return null;
    for (var i = 0; i < segs.length; i++) {
      var clean = true;
      for (var k = 1; k < segs[i].length; k++) if (ONSET0[segs[i][k]]) clean = false;
      if (clean) return segs[i];
    }
    return segs[0];
  }
  HEL.segment = segment;
  HEL.syllables = syllables;
  HEL.isTranslit = function (w) { return segment(w).length > 0; };

  /* ---------------------------------------------------------------- parsing */
  function ParseError(msg) { this.message = msg; }

  function parseWord(text) {
    var eq = text.indexOf("=");
    var word = eq >= 0 ? text.slice(0, eq) : text;
    var coord = eq >= 0 ? text.slice(eq + 1) : null;
    var ms = word.split("-");
    for (var i = 0; i < ms.length; i++) if (!ms[i]) throw new ParseError("an empty morpheme in " + text);
    var nw = { root: null, head: null, incidence: null, tail: null, grade: null, unent: false,
               discharge: null, polarity: null, rscope: null, scope: false, coord: null };
    if (ms.length > 1 && HEADS[ms[0]] && !SUFFIX[ms[1]]) { nw.head = HEADS[ms[0]]; ms = ms.slice(1); }
    nw.root = ms[0];
    if (!segment(nw.root).length) throw new ParseError("“" + nw.root + "” is not built from the sanctioned syllable list");
    var last = -1;
    for (var k = 1; k < ms.length; k++) {
      var m = ms[k], slot = SUFFIX[m];
      if (!slot) throw new ParseError("“" + m + "” is not a suffix formative (in " + text + ")");
      if (ORDER[slot] <= last) throw new ParseError("“" + m + "” (" + slot + ") is out of template order in " + text);
      last = ORDER[slot];
      if (slot === "tail") nw.tail = TAILS[m];
      else if (slot === "unent") nw.unent = true;
      else if (slot === "scope") nw.scope = true;
      else nw[slot] = m;
    }
    if (coord !== null) {
      var parts = coord ? coord.split("-") : [];
      var slots = [parts[0] || null, parts[1] || null, parts[2] || null];
      nw.coord = { locus: slots[0], pass: slots[1], phase: slots[2] };
    }
    return nw;
  }

  HEL.parseSegment = function (text) {
    var t = text.replace(/[•‧∙*]/g, "·").replace(/\s+/g, " ").trim();
    var chunks = t.split("·").map(function (c) { return c.trim(); }).filter(Boolean);
    var seg = { words: [], warrants: [], free: [] };
    chunks.forEach(function (c) {
      var toks = c.split(" ");
      if (toks.every(function (x) { return WARRANTS[x]; })) seg.warrants = seg.warrants.concat(toks);
      else if (toks.length === 1 && RITUAL[toks[0]]) seg.free.push(toks[0]);
      else if (toks.length === 1) seg.words.push(parseWord(toks[0]));
      else throw new ParseError("cannot read “" + c + "”: separate node words with ·");
    });
    return seg;
  };
  HEL.ParseError = ParseError;

  /* ---------------------------------------------------------------- grammar */
  function morphemes(w) {
    var m = [];
    if (w.head) m.push(["head", INV.edge_classes[w.head].head]);
    m.push(["root", w.root]);
    if (w.incidence) m.push(["incidence", w.incidence]);
    if (w.tail) m.push(["tail", INV.edge_classes[w.tail].tail]);
    if (w.grade) m.push(["grade", w.grade]);
    if (w.unent) m.push(["unent", "lar"]);
    if (w.discharge) m.push(["discharge", w.discharge]);
    if (w.polarity) m.push(["polarity", w.polarity]);
    if (w.rscope) m.push(["rscope", w.rscope]);
    if (w.scope) m.push(["scope", "he"]);
    return m;
  }
  function coordText(c) { return [c.locus, c.pass, c.phase].map(function (x) { return x || ""; }).join("-"); }
  function wordText(w) {
    var s = morphemes(w).map(function (x) { return x[1]; }).join("-");
    if (w.coord) s += "=" + coordText(w.coord);
    return s;
  }
  HEL.wordText = wordText;
  HEL.translit = function (seg) {
    var parts = seg.words.map(wordText).concat(seg.free);
    if (seg.warrants.length) parts.push(seg.warrants.join(" "));
    return parts.join(" · ");
  };
  HEL.tokens = function (seg) {
    var out = [];
    seg.words.forEach(function (w) {
      morphemes(w).forEach(function (m) { out.push(m[1]); });
      if (w.coord) [w.coord.locus, w.coord.pass, w.coord.phase].forEach(function (x) { if (x) out.push(x); });
    });
    return out.concat(seg.free, seg.warrants);
  };

  function edges(seg) {
    var ws = seg.words, n = ws.length, out = [];
    var tu = [], hu = [];
    for (var i = 0; i < n; i++) { tu.push(false); hu.push(false); }
    for (i = 0; i < n - 1; i++) {
      var a = ws[i], b = ws[i + 1];
      if (a.tail && b.head && !tu[i] && !hu[i + 1]) {
        out.push({ origin: i, dest: i + 1, cls: a.tail, kind: a.tail === b.head ? "complete" : "mismatch" });
        tu[i] = hu[i + 1] = true;
      } else if (a.head && b.tail && !hu[i] && !tu[i + 1] && a.head === b.tail) {
        out.push({ origin: i + 1, dest: i, cls: b.tail, kind: "complete" });
        tu[i + 1] = hu[i] = true;
      }
    }
    for (i = 0; i < n - 1; i++) {
      if (ws[i].tail && !tu[i] && !ws[i + 1].head) {
        out.push({ origin: i, dest: i + 1, cls: ws[i].tail, kind: "reduced" }); tu[i] = true;
      }
    }
    for (i = 0; i < n; i++) {
      if (ws[i].tail && !tu[i]) out.push({ origin: i, dest: null, cls: ws[i].tail, kind: "broken-tail" });
      if (ws[i].head && !hu[i]) out.push({ origin: null, dest: i, cls: ws[i].head, kind: "broken-head" });
    }
    return out;
  }
  HEL.edges = edges;

  /* Tail-only forms the Archive has identified as constructions, not damage
     (hel/grammar.py construction). The nine pairs HEL has not identified stay D-BROKEN. */
  function construction(w) {
    if (w.root === "kalsira" && w.tail === "PASS") return ["N-PAIR", "the bound pair kalsira-ru: the tail projects no edge (Keele 1963, A §10.1a)"];
    if (w.root === "lartuki" && w.tail === "RECUR") return ["N-PAIR", "the bound pair lartuki-halu (the 1969 paraphrase, A §10.1b)"];
    if (w.polarity === "mun" && w.tail) return ["N-HALFNEG", "-mun on the tail half alone: a half-negated edge (A §4.4)"];
    return null;
  }
  HEL.construction = construction;

  HEL.check = function (seg, channel) {
    channel = channel || "Ch-1";
    var f = [], ws = seg.words, es = edges(seg);
    function add(code, sev, where, msg) { f.push({ code: code, severity: sev, where: where, message: msg }); }
    ws.forEach(function (w, k) {
      var where = "word " + (k + 1) + " (" + w.root + ")";
      if (!REG[w.root] && !RITUAL[w.root]) add("N-UNREG", "note", where, "not in the unit register; parsed by position");
      if ((w.grade || w.polarity || w.unent || w.discharge || w.rscope || w.scope) && !w.tail)
        add("E-EDGELESS", "ill-formed", where, "grade and polarity sit on the edge, and this word bears no tail");
      if ((w.unent || w.discharge) && !w.grade) add("E-UNGRADED", "ill-formed", where, "UNENT and discharge need a grade");
      if (w.unent && w.grade !== "lan" && w.grade !== "kas") add("E-UNENT", "ill-formed", where, "UNENT marks AUTH or EXEC only");
      if (w.rscope && !w.polarity) add("E-RSCOPE", "ill-formed", where, "recurrence scope needs a polarity");
      if (w.scope && !w.polarity) add("E-SCOPE", "ill-formed", where, "the scope clitic needs a polarity");
      if (w.incidence === "ol") {
        es.forEach(function (e) {
          if ((e.origin === k || e.dest === k) && e.cls !== "BIND") {
            var o = e.origin !== null ? ws[e.origin] : null;
            if (!o || o.grade !== "ti") add("E-OFF", "ill-formed", where, "an OFF node takes no motion edge unless it is SIM-graded");
          }
        });
      }
      if (w.coord) {
        if (!w.head) add("E-CARRIER", "ill-formed", where, "only a head-bearing word carries a coordinate");
        else {
          var into = es.filter(function (e) { return e.dest === k && e.kind === "complete"; });
          if (!into.length && w.tail === w.head) add("E-ANCHOR", "ill-formed", where, "carrier and anchor collapse into one word: the coordinate does not compose");
          else if (!into.length) add("D-ANCHOR", "damaged", where, "the anchor word is missing: the coordinate is intact and unreadable");
        }
        [["LOCUS", w.coord.locus], ["PASS", w.coord.pass], ["PHASE", w.coord.phase]].forEach(function (s) {
          if (!s[1]) add("D-SLOT", "damaged", where, s[0] + " slot absent, not ruled empty");
        });
        if (w.coord.pass && w.coord.pass !== GAP && !PASSV[w.coord.pass]) add("E-PASS", "ill-formed", where, "“" + w.coord.pass + "” is not a PASS value");
        if (w.coord.phase && w.coord.phase !== GAP && !PHASEV[w.coord.phase]) add("E-PHASE", "ill-formed", where, "“" + w.coord.phase + "” is not a PHASE value");
      }
    });
    es.forEach(function (e) {
      if (e.kind === "mismatch") add("E-AGREE", "ill-formed", "words " + (e.origin + 1) + "–" + (e.dest + 1), "edge halves disagree in class");
      if (e.kind === "broken-tail") {
        var known = construction(ws[e.origin]);
        if (known) add(known[0], "note", "word " + (e.origin + 1), known[1]);
        else add("D-BROKEN", "damaged", "word " + (e.origin + 1), "-" + INV.edge_classes[e.cls].tail + " ⌀ (broken half)");
      }
      if (e.kind === "broken-head") add("D-BROKEN", "damaged", "word " + (e.dest + 1), "⌀ " + INV.edge_classes[e.cls].head + "- (broken half)");
    });
    if (!seg.warrants.length) add("D-WARRANT", "damaged", "segment", "no warrant: catalogued as damaged");
    return f;
  };
  HEL.wellFormed = function (seg, ch) { return !HEL.check(seg, ch).some(function (x) { return x.severity === "ill-formed"; }); };

  HEL.profile = function (seg) {
    var es = edges(seg);
    var reduced = es.some(function (e) { return e.kind === "reduced"; });
    var stacked = seg.warrants.length > 1;
    var scope = seg.words.some(function (w) { return w.scope; });
    var pol = seg.words.some(function (w) { return w.polarity; });
    if (stacked || scope) return "I";
    if (reduced || pol) return "II";
    return "I/II";
  };

  HEL.reverse = function (seg, idx) {
    var copy = JSON.parse(JSON.stringify(seg));
    var complete = edges(seg).filter(function (e) { return e.kind === "complete"; });
    var e = complete[idx || 0];
    if (!e) return null;
    var o = copy.words[e.origin];
    o.tail = null; o.grade = null; o.polarity = null; o.scope = false; o.unent = false; o.discharge = null; o.rscope = null;
    copy.words[e.dest].tail = e.cls;
    return copy;
  };

  /* ---------------------------------------------------------------- gloss */
  function q(slot, form) {
    var x = INV.slots[slot][form];
    return x.abbr + (x.grade === "G3" ? "?" : "");
  }
  function edgeAbbr(cls, half) { return cls + "." + half + (INV.edge_classes[cls].grade === "G3" ? "?" : ""); }
  function catalogGloss(form) {
    var u = REG[form];
    if (!u) return "[" + form + "]";
    var num = u.cid.replace("CSC-", "CSC.");
    return u.gloss ? num + "(" + u.gloss + "?)" : num + "(?)";
  }
  HEL.catalogGloss = catalogGloss;
  function glossWord(w) {
    return morphemes(w).map(function (m) {
      if (m[0] === "head") return edgeAbbr(w.head, "HEAD");
      if (m[0] === "tail") return edgeAbbr(w.tail, "TAIL");
      if (m[0] === "root") return catalogGloss(m[1]);
      return q(m[0], m[1]);
    }).join("-");
  }
  function glossCoord(c) {
    var names = ["LOC", "PASS", "PHASE"], vals = [c.locus, c.pass, c.phase];
    return "=" + vals.map(function (v, i) {
      if (!v) return names[i] + ".⌀";
      if (v === GAP) return names[i] + ".GAP";
      if (i === 0) return catalogGloss(v);
      if (i === 1) return PASSV[v] ? q("pass", v) : "[" + v + "]";
      return PHASEV[v] ? q("phase", v) : "[" + v + "]";
    }).join("-");
  }
  HEL.gloss = function (seg) {
    var cols = [];
    seg.words.forEach(function (w) {
      cols.push([wordText(w).split("=")[0], glossWord(w)]);
      if (w.coord) cols.push(["=" + coordText(w.coord), glossCoord(w.coord)]);
    });
    seg.free.forEach(function (u) { cols.push([u, catalogGloss(u)]); });
    seg.warrants.forEach(function (wr) {
      cols.push([wr, wr === "[41]" ? "(warrant slot; no value assigned)" : q("warrant", wr)]);
    });
    return cols;
  };

  /* ---------------------------------------------------------------- readback */
  var NUMW = { 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven" };
  function cap(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : s; }
  HEL.readback = function (seg) {
    var RB = INV.readback, turnA = [], b = [], edgesSaid = [];
    turnA.push(seg.words.map(function (w) { return cap(wordText(w).split("=")[0]); }).join(", ") + ".");
    var coords = seg.words.filter(function (w) { return w.coord; }).map(function (w) { return w.coord; });
    if (coords.length) turnA.push(cap([coords[0].locus, coords[0].pass, coords[0].phase].map(function (x) { return x || "—"; }).join("-")) + ".");
    if (seg.warrants.length) turnA.push(cap(seg.warrants.join(" ")) + ".");
    seg.words.forEach(function (w) {
      var bits = [cap(w.root)];
      if (w.incidence) bits.push(RB[INV.slots.incidence[w.incidence].abbr]);
      if (w.tail) { var ew = "edge " + NUMW[INV.edge_number[w.tail]]; bits.push(ew); edgesSaid.push(ew); }
      if (w.grade) bits.push(RB[INV.slots.grade[w.grade].abbr]);
      if (w.polarity) bits.push(RB[INV.slots.polarity[w.polarity].abbr]);
      b.push(bits.join(", ") + ".");
    });
    coords.forEach(function (c) {
      var parts = [];
      [["LOC", c.locus], ["PASS", c.pass], ["PHASE", c.phase]].forEach(function (p) {
        var v = p[1];
        if (!v) parts.push(p[0].toLowerCase() + " lost");
        else if (v === GAP) parts.push(RB[p[0] + ".GAP"]);
        else if (p[0] === "LOC") parts.push("locus " + v);
        else if (p[0] === "PASS") parts.push(PASSV[v] ? RB[PASSV[v].abbr] : v);
        else parts.push(PHASEV[v] ? RB[PHASEV[v].abbr] : v);
      });
      b.push(cap(parts.join(", ")) + ".");
    });
    if (seg.warrants.length) b.push(cap(seg.warrants.map(function (w) { return RB[WARRANTS[w].abbr]; }).join(", ")) + ".");
    return [turnA.join(" "), b.join(" "), "Confirmed" + edgesSaid.map(function (e) { return ", " + e; }).join("") + "."];
  };

  /* ---------------------------------------------------------------- pronunciation */
  var IPA_C = { p: "p", t: "t", k: "k", s: "s", h: "h", m: "m", n: "n", l: "l", r: "ɹ", w: "w", y: "j", f: "f" };
  var IPA_V = { standard: { a: "a", e: "e", i: "i", o: "o", u: "u" }, chicago: { a: "a", e: "eɪ", i: "i", o: "oʊ", u: "u" } };
  function ipaSyl(s, trad) { return s.split("").map(function (c) { return IPA_C[c] || IPA_V[trad][c] || c; }).join(""); }
  function ipaMorph(m, trad) { var s = syllables(m); return s ? s.map(function (x) { return ipaSyl(x, trad); }) : [m]; }
  HEL.ipa = function (seg, trad) {
    trad = trad || "standard";
    var words = [];
    seg.words.forEach(function (w) {
      var parts = [];
      morphemes(w).forEach(function (m) {
        var sy = ipaMorph(m[1], trad);
        if (m[0] === "root") sy[sy.length - 1] = "ˈ" + sy[sy.length - 1];
        parts = parts.concat(sy);
      });
      words.push(parts.join("."));
      if (w.coord) [w.coord.locus, w.coord.pass, w.coord.phase].forEach(function (v) {
        if (!v) return;
        var sy = ipaMorph(v, trad); sy[sy.length - 1] = "ˈ" + sy[sy.length - 1]; words.push(sy.join("."));
      });
    });
    seg.free.concat(seg.warrants).forEach(function (u) {
      if (u === "[41]") { words.push("ˈfɔɹti ˈwʌn"); return; }
      var sy = ipaMorph(u, trad); sy[sy.length - 1] = "ˈ" + sy[sy.length - 1]; words.push(sy.join("."));
    });
    return "[" + words.join(" ") + "]";
  };

  /* The Second branch: *Common Recitation through S2 (k > h before i) and S3
     (unstressed e > i, o > u); head halves lost (H4); stress initial. */
  function second(form, stressed) {
    if (SECOND_IRR[form]) return SECOND_IRR[form];
    var cr = COMMON[form] || form;
    var s = cr.replace(/ki/g, "hi");
    var vs = []; for (var i = 0; i < s.length; i++) if ("aeiou".indexOf(s[i]) >= 0) vs.push(i);
    var arr = s.split("");
    (stressed ? vs.slice(1) : vs).forEach(function (j) { if (arr[j] === "e") arr[j] = "i"; else if (arr[j] === "o") arr[j] = "u"; });
    return arr.join("");
  }
  HEL.second = second;
  HEL.recite = function (seg, branch) {
    var words = [];
    seg.words.forEach(function (w) {
      var ms = morphemes(w).filter(function (m) { return !(branch === "second" && m[0] === "head"); });
      var out = ms.map(function (m, i) {
        if (branch !== "second") return ipaMorph(m[1], "chicago").join("");
        return second(m[1], m[0] === "root");
      }).join("-");
      if (w.coord) out += "=" + [w.coord.locus, w.coord.pass, w.coord.phase].map(function (v) {
        if (!v) return "⌀";
        return branch === "second" ? second(v, true) : ipaMorph(v, "chicago").join("");
      }).join("-");
      words.push(branch === "second" ? "ˈ" + out : out);
    });
    seg.free.forEach(function (u) { words.push(branch === "second" ? "ˈ" + second(u, true) : ipaMorph(u, "chicago").join("")); });
    seg.warrants.forEach(function (u) { words.push(u === "[41]" ? "ˈfɔɹti ˈwʌn" : (branch === "second" ? "ˈ" + second(u, true) : ipaMorph(u, "chicago").join(""))); });
    return words.join(" · ");
  };

  /* ---------------------------------------------------------------- layer 4 */
  /* The Archive's operational English (A §6.3), with the residue printed under it:
     "every gloss states its residue" (benchmark C5). */
  HEL.translate = function (seg) {
    var ws = seg.words, es = edges(seg), out = [], residue = [], N = ws.map(function (w) { return w.root.toUpperCase(); });
    var motion = es.filter(function (e) { return e.dest !== null && e.origin !== null && ["PASS", "THRU"].indexOf(e.cls) >= 0 && e.kind !== "mismatch"; });
    if (ws.length === 1 && !es.length) {
      var inc = { "in": "terminal", "is": "traversed through", "ar": "a junction (other edges attach, not stated)", "ol": "referenced, off-path" }[ws[0].incidence];
      out.push("Label: " + N[0] + (inc ? ", " + inc : "") + ".");
    } else if (motion.length && motion.length === es.filter(function (e) { return e.dest !== null && e.origin !== null; }).length) {
      var chain = [N[0]];
      for (var i = 1; i < ws.length; i++) {
        var into = es.filter(function (e) { return e.dest === i; })[0];
        chain.push((into && into.cls === "THRU" && ws[i].incidence === "is" ? "via " : "") + N[i]);
      }
      out.push("Route: " + chain.join(" → ") + ".");
    }
    es.forEach(function (e) {
      var A = e.origin !== null ? N[e.origin] : "(origin lost)", B = e.dest !== null ? N[e.dest] : "(destination lost)";
      if (e.kind === "broken-tail") out.push(A + ": an edge departs; its destination is lost (-" + INV.edge_classes[e.cls].tail + " ⌀).");
      else if (e.kind === "broken-head") out.push(B + ": an edge arrives; its origin is lost.");
      else if (e.cls === "SHUNT") out.push(A + " → " + B + ": arrival displaced from intent.");
      else if (e.cls === "BAR") out.push("The edge " + A + " → " + B + " is present and not traversable in this orientation.");
      else if (e.cls === "RECUR") out.push(A + " → " + B + ": a return to a similar, non-identical coordinate.");
      else if (e.cls === "BIND") out.push(A + " and " + B + " are one coordinate under two descriptions.");
      else if (e.cls === "ADJ") out.push(A + " and " + B + " adjacent; orientation not recovered.");
      if (e.kind === "reduced") residue.push("The head half of " + A + " → " + B + " is absent (the Stratum II profile); the direction is taken from the Standard's writing order.");
      if (e.origin === null) return;
      var w = ws[e.origin];
      if (w.grade) out.push({ ti: "Modeled only; no commitment.", ka: "Staged.", lan: "Authorized — a restricted form (Field Protocol).", kas: "Executed or executing." }[w.grade] +
        (w.unent ? " Without entitlement — or, on the other reading, recorded with the permission bit clear." : "") +
        (w.discharge ? " " + { lun: "Still in force; no release recorded.", ro: "Discharged.", sar: "Lapsed without discharge.", ki: "In force under a condition the record does not state.", le: "Discharge not stated." }[w.discharge] : ""));
      if (w.polarity) {
        out.push({ mun: "No such edge.", sen: "Closed — by what, not stated.", nir: "Not available at this coordinate.", lus: "This record does not establish the edge's status." }[w.polarity] +
          (w.rscope ? " " + { li: "(At this pass.)", kur: "(At every recurrence.)", ra: "(Recurrence scope not stated.)" }[w.rscope] : ""));
        if (w.polarity === "sen") residue.push("English 'forbidden' would supply a forbidder; the record names none.");
        if (!ws.some(function (x) { return x.scope; }) && w.polarity === "sen") residue.push("No scope clitic: whether the closure governs the edge or the whole segment is not recorded.");
      }
    });
    ws.forEach(function (w) {
      if (!w.coord) return;
      var c = w.coord, s = [];
      s.push(!c.locus ? "Locus slot lost." : c.locus === GAP ? "Emergence locus not recorded." : "Emergence locus in the " + catalogGloss(c.locus) + " state.");
      s.push(!c.pass ? "Pass slot lost." : ({ sa: "This pass.", to: "A later pass.", nu: "Another pass, order not recorded.", hilun: "Pass not recorded." })[c.pass] || "");
      s.push(!c.phase ? "Phase slot lost." : ({ kihar: "At the anchor phase.", pukal: "Phase displacement measured, ahead — magnitude not stated.", rolun: "Phase displacement measured, behind — magnitude not stated.", nikur: "Displaced; not measured.", hilun: "Phase not recorded." })[c.phase] || "");
      out.push(s.join(" "));
      if (c.pass && c.pass !== GAP && c.phase && c.phase !== GAP) residue.push("English 'later' would merge pass-order and phase; the record states them separately.");
      if (c.locus === GAP) residue.push("'Not recorded' is weaker than hilun: the record says that it does not have the value.");
      if (c.phase === "pukal" || c.phase === "rolun") residue.push("No magnitude is in any record (A §5.2b).");
    });
    if (seg.free.length) out.push(seg.free.map(function (u) { return u.toUpperCase(); }).join(", ") + ": not translated.");
    var W = seg.warrants;
    if (W.length === 2 && W[0] === "lekur" && W[1] === "hos") out.push("Recurrent, and inferred.");
    else if (W.length === 2 && W[0] === "hos" && W[1] === "lekur") out.push("Inferred to be recurrent.");
    else if (W.length) {
      var ph = W.map(function (w) { return { nes: "entered without a human attestor", tir: "attested on site", lekur: "observed on more than one pass", hos: "derived from other edges", wal: "no source carried", "[41]": "forty-one" }[w]; });
      out.push(cap(ph.join("; ")) + ".");
    }
    if (W.length === 1 && W[0] === "lekur") residue.push("Style manual: a segment warranted lekur alone is never translated with 'because'.");
    if (W.length === 2) residue.push("Stacked warrants: order is scope.");
    if (ws.length) residue.push("The capitalised names are HEL's designators for catalogue roots, not translations; every root is queried (A §6.3).");
    return { text: out.join(" "), residue: residue };
  };

  /* ---------------------------------------------------------------- the trace */
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(seed) { var x = seed || 1; return function () { x ^= x << 13; x ^= x >>> 17; x ^= x << 5; return ((x >>> 0) % 10000) / 10000; }; }
  var C = {
    groove: "stroke:var(--groove,#2B3440)", hi: "stroke:var(--chalk,#FDFDF8)", fill: "fill:var(--groove,#2B3440)",
    paper: "fill:var(--paper,#F3F4EF)", lead: "stroke:var(--ink-2,#4A5463)", dmg: "stroke:var(--warn,#9A5B12)",
    faint: "stroke:var(--rule,#C5CBC2)", stamp: "stroke:var(--stamp,#5B3C8F)"
  };
  function line(x1, y1, x2, y2, st, w, extra) {
    return '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) +
      '" style="' + st + ';stroke-width:' + (w || 2.2) + ';stroke-linecap:round;fill:none' + (extra || "") + '"/>';
  }
  function path(d, st, w, extra) {
    return '<path d="' + d + '" style="' + st + ';stroke-width:' + (w || 2.2) + ';stroke-linecap:round;stroke-linejoin:round;fill:none' + (extra || "") + '"/>';
  }
  function incised(d, w) {
    // a groove with a highlight one unit below-right: the look of a cut, in either theme
    return path(d, C.hi, (w || 2.4) + 1.2, ";opacity:.55;transform:translate(0.6px,0.9px)") + path(d, C.groove, w || 2.4);
  }
  function circle(cx, cy, r, st, filled) {
    return '<circle cx="' + cx.toFixed(1) + '" cy="' + cy.toFixed(1) + '" r="' + r + '" style="' +
      (filled ? C.fill + ";stroke:none" : st + ";stroke-width:1.6;fill:none") + '"/>';
  }
  var NOTCH_W = 11;
  function cluster(form, x, y, scale) {
    // one notch group per syllable (the 1908 stipulation); shapes fixed by the unit's
    // identity, never by its spelling — the trace carries no phonology (A §6.1)
    scale = scale || 1;
    var sy = syllables(form) || [form], r = rng(hash(form) || 7), out = "";
    for (var i = 0; i < sy.length; i++) {
      var cx = x + i * NOTCH_W * scale, t = Math.floor(r() * 7), h = (9 + r() * 7) * scale, lean = (r() - 0.5) * 6 * scale;
      if (t === 0) out += incised("M" + (cx + lean).toFixed(1) + " " + (y - h).toFixed(1) + " L" + (cx - lean).toFixed(1) + " " + (y + h).toFixed(1), 2.1 * scale);
      else if (t === 1) out += incised("M" + cx.toFixed(1) + " " + y + " L" + (cx + lean).toFixed(1) + " " + (y - h - 3 * scale).toFixed(1), 2.1 * scale);
      else if (t === 2) out += incised("M" + cx.toFixed(1) + " " + y + " L" + (cx + lean).toFixed(1) + " " + (y + h + 3 * scale).toFixed(1), 2.1 * scale);
      else if (t === 3) out += circle(cx, y - 9 * scale, 2.3 * scale, C.groove, true) + circle(cx, y - 9 * scale, 2.3 * scale, C.groove, false);
      else if (t === 4) out += circle(cx, y + 9 * scale, 2.3 * scale, C.groove, true);
      else if (t === 5) out += incised("M" + cx.toFixed(1) + " " + y + " L" + cx.toFixed(1) + " " + (y - h).toFixed(1) + " l" + (4 * scale) + " " + (3 * scale), 2 * scale);
      else out += incised("M" + (cx - 2 * scale).toFixed(1) + " " + (y - h * 0.8).toFixed(1) + " L" + (cx - 2 * scale).toFixed(1) + " " + (y + h * 0.8).toFixed(1), 1.6 * scale) +
        incised("M" + (cx + 2 * scale).toFixed(1) + " " + (y - h * 0.8).toFixed(1) + " L" + (cx + 2 * scale).toFixed(1) + " " + (y + h * 0.8).toFixed(1), 1.6 * scale);
    }
    return { svg: out, width: sy.length * NOTCH_W * scale };
  }
  HEL.cluster = cluster;

  function flickClass(cls, x1, x2, y, kind) {
    // the interval between clusters: the edge, spelled by its silhouette
    var mid = (x1 + x2) / 2, out = "", d;
    if (kind === "illegible" || cls === "ADJ") {
      return path("M" + x1 + " " + y + " L" + x2 + " " + y, C.dmg, 2, ";stroke-dasharray:2 5;opacity:.85");
    }
    if (cls === "BIND") {
      return incised("M" + x1 + " " + (y - 3) + " L" + x2 + " " + (y - 3), 1.8) + incised("M" + x1 + " " + (y + 3) + " L" + x2 + " " + (y + 3), 1.8);
    }
    if (cls === "SHUNT") {
      var q1 = x1 + (x2 - x1) * 0.3, q2 = x1 + (x2 - x1) * 0.5, q3 = x1 + (x2 - x1) * 0.7;
      d = "M" + x1 + " " + y + " L" + q1 + " " + y + " L" + q2 + " " + (y - 11) + " L" + q2 + " " + (y + 9) + " L" + q3 + " " + y + " L" + x2 + " " + y;
      return incised(d);
    }
    if (cls === "RECUR") {
      d = "M" + x1 + " " + y + " L" + (mid - 6) + " " + y + " C" + (mid + 10) + " " + y + " " + (mid + 10) + " " + (y - 18) + " " + mid + " " + (y - 18) +
        " C" + (mid - 10) + " " + (y - 18) + " " + (mid - 10) + " " + y + " " + (mid + 6) + " " + y + " L" + x2 + " " + y;
      return incised(d);
    }
    d = "M" + x1 + " " + y + " Q" + mid + " " + (y - 13) + " " + x2 + " " + y;
    out = incised(d);
    if (cls === "THRU") out += incised("M" + (x1 + 8) + " " + (y - 13) + " l3 9 M" + (x1 + 14) + " " + (y - 14) + " l3 9", 1.8);
    if (cls === "BAR") out += incised("M" + (x1 + 3) + " " + (y - 15) + " L" + (x1 + 3) + " " + (y + 6) + " M" + (x1 - 3) + " " + (y - 15) + " L" + (x1 + 9) + " " + (y - 15), 2.2);
    return out;
  }
  function arrivalBarb(x, y) { return incised("M" + (x - 7) + " " + (y - 7) + " L" + x + " " + y + " L" + (x - 8) + " " + (y + 3), 1.9); }
  function departure(x, y) { return incised("M" + x + " " + y + " l6 -5", 1.9); }

  function gradeMark(w, x, y) {
    var out = "", g = w.grade;
    if (!g) return out;
    var gy = y - 24;
    if (g === "ti") out += path("M" + (x - 5) + " " + gy + " q5 -7 10 0", C.groove, 1.6, ";stroke-dasharray:2 2.5");
    else if (g === "ka") out += line(x, gy - 5, x, gy + 3, C.groove, 1.9);
    else if (g === "lan") out += line(x - 5, gy, x + 5, gy, C.groove, 1.7) + line(x - 3, gy - 4, x + 3, gy + 4, C.groove, 1.7) + line(x - 3, gy + 4, x + 3, gy - 4, C.groove, 1.7);
    else if (g === "kas") out += circle(x, gy, 3, C.groove, true);
    if (w.unent) out += line(x - 7, gy + 6, x + 7, gy - 7, C.stamp, 1.8);
    var dx = x + 11;
    if (w.discharge === "lun") out += circle(dx, gy, 3.2, C.groove, false);
    else if (w.discharge === "ro") out += '<rect x="' + (dx - 3) + '" y="' + (gy - 3) + '" width="6" height="6" style="' + C.fill + '"/>';
    else if (w.discharge === "ki") out += path("M" + (dx + 2) + " " + (gy - 5) + " h-3 v10 h3", C.groove, 1.5);
    else if (w.discharge === "sar") out += path("M" + (dx - 3) + " " + gy + " a3 3 0 0 1 6 0", C.groove, 1.6);
    else if (w.discharge === "le") out += '<rect x="' + (dx - 3) + '" y="' + (gy - 3) + '" width="6" height="6" style="' + C.groove + ';stroke-width:1.2;fill:none"/>';
    return out;
  }
  function polarityMark(w, x, y) {
    var out = "", p = w.polarity;
    if (!p) return out;
    if (p === "mun") out += line(x - 6, y - 6, x + 6, y + 6, C.groove, 2.2) + line(x - 6, y + 6, x + 6, y - 6, C.groove, 2.2);
    else if (p === "sen") out += line(x, y - 10, x, y + 10, C.groove, 2.6);
    else if (p === "nir") out += '<rect x="' + (x - 4) + '" y="' + (y - 4) + '" width="8" height="8" style="' + C.paper + ';stroke:none"/>' + line(x - 4, y - 5, x - 4, y + 5, C.groove, 1.6) + line(x + 4, y - 5, x + 4, y + 5, C.groove, 1.6);
    else if (p === "lus") out += path("M" + (x - 3) + " " + (y - 9) + " q6 -3 5 3 q-1 3 -2 5", C.groove, 1.7);
    if (w.rscope === "li") out += circle(x, y + 14, 1.8, C.groove, true);
    else if (w.rscope === "kur") out += circle(x, y + 14, 3.4, C.groove, false) + circle(x, y + 14, 1.6, C.groove, false);
    else if (w.rscope === "ra") out += '<rect x="' + (x - 2.5) + '" y="' + (y + 11.5) + '" width="5" height="5" style="' + C.groove + ';stroke-width:1.1;fill:none"/>';
    if (w.scope) out += path("M" + (x - 16) + " " + (y - 20) + " Q" + x + " " + (y - 30) + " " + (x + 16) + " " + (y - 20), C.groove, 1.3);
    return out;
  }
  function cartouche(c, x, y) {
    var w = 72, h = 26, cw = w / 3, out = "";
    out += '<rect x="' + x + '" y="' + (y - h / 2) + '" width="' + w + '" height="' + h + '" rx="11" style="' + C.paper + ';' + C.groove + ';stroke-width:2.2"/>';
    out += line(x + cw, y - h / 2 + 3, x + cw, y + h / 2 - 3, C.groove, 1.1) + line(x + 2 * cw, y - h / 2 + 3, x + 2 * cw, y + h / 2 - 3, C.groove, 1.1);
    [c.locus, c.pass, c.phase].forEach(function (v, i) {
      var cx = x + cw * i + cw / 2;
      if (!v) { out += '<rect x="' + (cx - 8) + '" y="' + (y - 7) + '" width="16" height="14" style="' + C.dmg + ';stroke-width:1.2;fill:none;stroke-dasharray:2 2"/>'; return; }
      if (v === GAP) { out += line(cx - 7, y, cx + 7, y, C.groove, 1.2); return; }  // ruled empty
      if (i === 0) { var cl = cluster(v, cx - (syllables(v) || [1]).length * 3, y, 0.42); out += cl.svg; return; }
      if (v === "sa") out += circle(cx, y, 2.2, C.groove, true);
      else if (v === "to") out += circle(cx, y - 4, 2, C.groove, true) + circle(cx, y + 4, 2, C.groove, true);
      else if (v === "nu") out += circle(cx, y, 3.4, C.groove, false);
      else if (v === "kihar") out += line(cx - 6, y, cx + 6, y, C.groove, 2.2);
      else if (v === "pukal") out += line(cx - 6, y + 2, cx + 6, y + 2, C.groove, 2.2) + line(cx + 5, y + 2, cx + 5, y - 6, C.groove, 2);
      else if (v === "rolun") out += line(cx - 6, y - 2, cx + 6, y - 2, C.groove, 2.2) + line(cx - 5, y - 2, cx - 5, y + 6, C.groove, 2);
      else if (v === "nikur") out += path("M" + (cx - 7) + " " + y + " q2 -5 4 0 t4 0 t4 0", C.groove, 1.8);
      else out += '<text x="' + cx + '" y="' + (y + 3) + '" style="font:8px var(--mono,monospace);fill:var(--ink-2,#4A5463)" text-anchor="middle">?</text>';
    });
    return { svg: out, width: w };
  }
  function warrantTick(wr, x, y) {
    if (wr === "nes") return path("M" + x + " " + (y + 6) + " L" + x + " " + (y - 6) + " l4 3", C.groove, 1.9);
    if (wr === "tir") return line(x, y - 7, x, y + 6, C.groove, 1.9) + circle(x + 4, y - 6, 1.6, C.groove, true);
    if (wr === "lekur") return line(x - 2, y - 6, x - 2, y + 6, C.groove, 1.8) + line(x + 3, y - 6, x + 3, y + 6, C.groove, 1.8);
    if (wr === "hos") return path("M" + (x - 5) + " " + (y + 5) + " L" + x + " " + (y - 6) + " L" + (x + 5) + " " + (y + 5) + " Z", C.groove, 1.6);
    if (wr === "wal") return circle(x, y, 4.2, C.groove, false);
    if (wr === "[41]") return path("M" + x + " " + y + " m0 0 a2 2 0 1 1 3 2 a4 4 0 1 1 -6 -5 a6 6 0 1 1 9 8", C.stamp, 1.5);
    return "";
  }

  HEL.traceSVG = function (seg, opts) {
    opts = opts || {};
    var ws = seg.words, es = edges(seg), y = 86, x = 26, parts = [], pos = [], gapW = 58;
    var byOrigin = {}, byDest = {};
    es.forEach(function (e) { if (e.origin !== null) byOrigin[e.origin] = e; if (e.dest !== null && e.kind !== "broken-tail") byDest[e.dest] = e; });
    var bh = byDest[0];
    if (bh && bh.kind === "broken-head") {
      parts.push(path("M" + (x - 4) + " " + (y - 9) + " l4 5 l-3 4 l4 6", C.dmg, 1.6));
      parts.push(incised("M" + x + " " + y + " L" + (x + 26) + " " + y)); parts.push(arrivalBarb(x + 26, y)); x += 30;
    }
    ws.forEach(function (w, k) {
      var off = w.incidence === "ol", cy = off ? y + 32 : y;
      var cl = cluster(w.root, x + 6, cy);
      if (off) parts.push(line(x + 6 + cl.width / 2, y, x + 6 + cl.width / 2, cy - 12, C.groove, 1.2) + incised("M" + x + " " + y + " L" + (x + cl.width + 10) + " " + y, 1.4));
      else parts.push(incised("M" + x + " " + y + " L" + (x + cl.width + 10) + " " + y));
      parts.push(cl.svg);
      var left = x, right = x + cl.width + 10;
      if (w.incidence === "in") {
        var endLeft = !w.head && !(byDest[k]), endRight = !w.tail;
        if (endLeft) parts.push(line(left - 2, y - 9, left - 2, y + 9, C.groove, 2.4));
        if (endRight && !w.coord) parts.push(line(right + 2, y - 9, right + 2, y + 9, C.groove, 2.4));
      } else if (w.incidence === "is") parts.push(circle(left + (right - left) / 2, y, 3.6, C.groove, false));
      else if (w.incidence === "ar") parts.push(incised("M" + (right - 4) + " " + y + " L" + (right + 10) + " " + (y + 17), 2));
      pos.push({ left: left, right: right });
      x = right;
      if (w.coord) {
        var ct = cartouche(w.coord, x + 4, y);
        parts.push(ct.svg); x += ct.width + 8;
        if (k < ws.length - 1) parts.push(incised("M" + (x - 4) + " " + y + " L" + x + " " + y));
      }
      var e = byOrigin[k];
      if (e) {
        var x1 = x, x2 = x + gapW;
        parts.push(departure(x1, y));
        if (e.kind === "broken-tail") {
          parts.push(incised("M" + x1 + " " + y + " L" + (x1 + 22) + " " + y));
          parts.push(path("M" + (x1 + 22) + " " + (y - 8) + " l-3 5 l4 4 l-3 6", C.dmg, 1.6));
          parts.push(gradeMark(w, x1 + 8, y) + polarityMark(w, x1 + 14, y));
          x = x1 + 30;
        } else {
          var illegible = ws[k].tail_illegible;
          parts.push(flickClass(e.cls, x1, x2, y, illegible ? "illegible" : ""));
          if (e.kind !== "reduced") parts.push(arrivalBarb(x2, y));
          parts.push(gradeMark(w, x1 + 8, y) + polarityMark(w, (x1 + x2) / 2, y));
          x = x2;
        }
      } else if (k < ws.length - 1) {
        // no edge between adjacent words (e.g. a head on the next word pairs backwards)
        var nx = ws[k + 1];
        if (nx.tail && w.head === nx.tail) { parts.push(flickClass(nx.tail, x, x + gapW, y, "")); parts.push(arrivalBarb(x, y)); x += gapW; }
        else { parts.push(path("M" + x + " " + y + " L" + (x + 20) + " " + y, C.faint, 1.4, ";stroke-dasharray:1 4")); x += 20; }
      }
    });
    // warrants: marginal ticks on lead-lines (A §9)
    var lastX = x, wy = y - 44;
    if (seg.warrants.length) {
      seg.warrants.forEach(function (wr, i) {
        var tx = lastX + 18 + i * 18;
        parts.push(path("M" + (lastX - 4) + " " + (y - 4) + " Q" + (tx - 4) + " " + (y - 14) + " " + tx + " " + (wy + 8), C.lead, 1, ";stroke-dasharray:1.5 3"));
        parts.push(warrantTick(wr, tx, wy));
      });
      x = lastX + 26 + seg.warrants.length * 18;
    } else if (opts.showLostWarrant !== false && ws.length) {
      parts.push(path("M" + (lastX - 4) + " " + (y - 4) + " Q" + (lastX + 6) + " " + (y - 14) + " " + (lastX + 10) + " " + (y - 24), C.lead, 1, ";stroke-dasharray:1.5 3"));
      parts.push(path("M" + (lastX + 7) + " " + (y - 30) + " l6 6 m0 -6 l-6 6", C.dmg, 1.4));
      x = lastX + 26;
    }
    var width = Math.max(x + 16, 120), height = 150;
    var label = opts.label ? ' aria-label="' + opts.label.replace(/"/g, "") + '"' : "";
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + width.toFixed(0) + " " + height + '" width="' + width.toFixed(0) + '" height="' + height + '" role="img"' + label + ">" + parts.join("") + "</svg>";
  };

  /* Stratum III: a field of marks with no line, no flicks, no cartouche.
     "A damaged segment is a sentence with a hole in it. A Stratum III sequence is
     not a sentence and has no hole." (A-reserve §2.2) */
  HEL.fieldSVG = function (units, opts) {
    opts = opts || {};
    var perRow = 3, rowH = 66, colW = 122, x0 = 30, y0 = 50, parts = [];
    var rows = Math.ceil(units.length / perRow);
    var w = x0 * 2 + perRow * colW - 34, h = y0 + rows * rowH - 8;
    // the marked field's extent: faint and dashed, because it is a boundary the
    // conservator drew, not a line the object carries (A-reserve §2.1, condition 2)
    parts.push('<rect x="8" y="10" width="' + (w - 16) + '" height="' + (h - 20) + '" rx="14" style="' + C.faint + ';stroke-width:1.2;fill:none;stroke-dasharray:3 6"/>');
    units.forEach(function (u, i) {
      var r = Math.floor(i / perRow), c = i % perRow;
      var cl = cluster(u, x0 + c * colW, y0 + r * rowH, 1.3);
      parts.push(cl.svg);
    });
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + " " + h + '" width="' + w + '" height="' + h + '" role="img" aria-label="Stratum III field">' + parts.join("") + "</svg>";
  };

  /* Stratum IV (Ch-3): sequence recoverable, shape not. A log tape, not a trace. */
  HEL.logSVG = function (units) {
    // one slot per logged unit, wide enough for its label; frame ticks every three
    var parts = [], x0 = 16, y = 40, xs = [], x = x0;
    units.forEach(function (u) { var wdt = Math.max(44, u.length * 6.4 + 12); xs.push([x, wdt]); x += wdt; });
    var w = x + x0, d = "M" + x0 + " " + y;
    for (var i = 0; i <= (w - 2 * x0) / 11; i++) { var xx = x0 + i * 11; d += " L" + xx.toFixed(1) + " " + (y + Math.sin(i * 1.7 + units.length) * 7).toFixed(1); }
    parts.push(path(d, C.faint, 1.2));
    units.forEach(function (u, i) {
      var cx = xs[i][0] + xs[i][1] / 2;
      if (i % 3 === 0) parts.push(line(xs[i][0], y - 22, xs[i][0], y + 22, C.lead, 1, ";stroke-dasharray:2 3"));
      parts.push('<text x="' + cx.toFixed(1) + '" y="' + (y + 36) + '" text-anchor="middle" style="font:10px var(--mono,monospace);fill:var(--ink-2,#4A5463)">' + u + "</text>");
      parts.push(circle(cx, y, 2, C.groove, true));
    });
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w.toFixed(0) + ' 86" width="' + w.toFixed(0) + '" height="86" role="img" aria-label="Ch-3 log">' + parts.join("") + "</svg>";
  };

  root.HEL = HEL;
  if (typeof module !== "undefined" && module.exports) module.exports = HEL;
})(typeof window !== "undefined" ? window : this);
