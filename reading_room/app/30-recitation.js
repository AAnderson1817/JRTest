/* Recitation: the Ch-4 formulae, the two branch traditions, and the code's own history. */
function formulaEntry(f) {
  for (var i = 0; i < D.entries.length; i++) {
    var e = D.entries[i];
    if (e.channel === "Ch-4" && e.segments.length && e.segments[0].translit === f.text) return e;
  }
  return null;
}
function colaHTML(seg, cola) {
  var syl = [];
  H.tokens(seg).forEach(function (t) { if (t !== "[41]") syl = syl.concat(H.syllables(t) || [t]); });
  var out = [], k = 0;
  cola.forEach(function (n) { out.push("<span>" + esc(syl.slice(k, k + n).join("-")) + "</span>"); k += n; });
  var ok = k === syl.length;
  return '<div class="cola">' + out.join("") + ' <i>+ forty-one</i></div><div class="label">' + cola.join(" · ") + " = " + k + " syllables" +
    (ok ? "" : " (count mismatch: " + syl.length + " in the text)") + " · [41] is said after the count and is not in it</div>";
}

function recitationCards() {
  return '<div class="formulae">' + D.formulae.map(function (f) {
    var seg = parse(f.text), e = formulaEntry(f);
    var warn = f.restricted ? '<div class="warnbar">Restricted. It carries an AUTH grade with STANDING discharge; Field Protocol keeps it inside the Reading Room (A §4.3). Crews call it the long word and have not heard it.</div>' : "";
    var b = f.b_dependent ? '<div class="label">Dependency: custodianship is Authority B</div>' : "";
    return '<div class="fcard"><h3>' + esc(f.name) + '</h3><div class="use">' + esc(f.use) + "</div>" + warn +
      '<div class="translit">' + esc(f.text) + "</div>" + colaHTML(seg, f.cola) +
      '<div class="br"><span class="k">Standard</span><span>' + esc(H.ipa(seg, "standard")) + '</span><span class="k">Chicago</span><span>' + esc(f.chicago) +
      '</span><span class="k">Second</span><span>' + esc(f.second) + "</span></div>" +
      (f.note ? '<div class="use">' + esc(f.note) + "</div>" : "") + b +
      (e ? '<div class="btns"><button class="btn alt" data-go="' + e.cid + '">' + esc(e.cid) + " in the catalogue</button></div>" : "") + "</div>";
  }).join("") + "</div>";
}

function lawList(steps) {
  if (!steps || !steps.length) return '<span class="quiet">no change</span>';
  return steps.map(function (s) { return esc(s[0].split(" ")[0]) + " " + esc(s[1]) + " → " + esc(s[2]); }).join("<br>");
}

function d2Table() {
  var rows = D.d2.rows.map(function (r) {
    var shib = r.chicago.replace(/eɪ/g, "e").replace(/oʊ/g, "o") !== r.second && /f/.test(r.second);
    return "<tr" + (shib ? ' class="new"' : "") + '><td class="m">' + esc(r.code_1988) + '</td><td class="m">' + esc(r.common) + '</td><td class="m">' + esc(r.chicago) +
      '</td><td class="m">' + esc(r.second) + '</td><td class="m">' + lawList(r.second_steps) + "</td></tr>";
  }).join("");
  return '<div class="tbl-wrap"><table><thead><tr><th>Code (1988)</th><th>*Common</th><th>Chicago</th><th>Second</th><th>Second-branch laws</th></tr></thead><tbody>' + rows + "</tbody></table></div>";
}

var GAME = { round: 0, score: 0, item: null, done: false, best: store.get("best", 0) };
function gamePick() {
  var pool = D.d2.rows.filter(function (r) { return r.second !== r.common.slice(1); });
  GAME.item = pool[Math.floor(Math.random() * pool.length)];
  GAME.done = false;
}
function renderGame() {
  var g = $("#game"), it = GAME.item;
  var stressed = D.d2.rootlike.indexOf(it.code_1988) >= 0;
  g.innerHTML = '<h3 class="label">Predict the Second branch · round ' + (GAME.round + 1) + " of 8 · score " + GAME.score + (GAME.best ? " · best " + GAME.best : "") + "</h3>" +
    "<p>The comparativists reconstruct <b class=\"mono\">" + esc(it.common) + "</b>" + (stressed ? ", a stressed word (stress on the first syllable)." : ", a bound formative, unstressed throughout.") +
    " What does the Second branch say?</p>" +
    '<form id="gform" class="btns"><input id="gin" autocomplete="off" spellcheck="false" aria-label="Your prediction"><button class="btn" type="submit">Check</button><button class="btn alt" type="button" id="gnext">' + (GAME.round >= 7 ? "Start again" : "Next") + "</button></form>" +
    '<div id="gres"></div><p class="intro">Laws, in order: S2 k becomes h before i; S3 unstressed e becomes i and o becomes u. S2 is older than S3 (Tredgold 1967), so a raised e never feeds S2.</p>';
  $("#gform").addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (GAME.done) return;
    var guess = $("#gin").value.trim().toLowerCase(), right = guess === it.second;
    GAME.done = true;
    if (right) GAME.score++;
    if (GAME.score > GAME.best) { GAME.best = GAME.score; store.set("best", GAME.best); }
    $("#gres").innerHTML = '<p class="' + (right ? "yes" : "no") + '">' + (right ? "Yes: " : "The Second branch says ") + '<span class="mono">' + esc(it.second) + "</span>.</p>" +
      '<p class="mono">' + lawList(it.second_steps) + "</p>";
  });
  $("#gnext").addEventListener("click", function () {
    if (GAME.round >= 7) { GAME.round = 0; GAME.score = 0; } else GAME.round++;
    gamePick(); renderGame();
  });
}

function d1Table() {
  var rows = D.d1.rows.map(function (r) {
    var status = r.irregular ? '<span class="no">' + esc(r.irregular) + "</span>" : '<span class="yes">regular</span>';
    return '<tr><td class="m">' + esc(r.form_1988) + '</td><td class="m">' + esc(r.form_1908) + '</td><td class="m">' + esc(r.heel || "—") +
      '</td><td class="m">' + lawList(r.steps) + "</td><td>" + status + "</td></tr>";
  }).join("");
  return '<div class="tbl-wrap"><table><thead><tr><th>1988</th><th>1908</th><th>Heel</th><th>Laws, in order</th><th>Status</th></tr></thead><tbody>' + rows + "</tbody></table></div>";
}

function reconstructionTable() {
  var mark = function (v) { return v ? '<span class="yes">accepts</span>' : '<span class="no">rejects</span>'; };
  return '<div class="tbl-wrap"><table><thead><tr><th>Law</th><th>Grade</th><th>Stated by</th><th>Utterance</th><th>Instrument</th><th>Palimpsest</th><th>The argument</th></tr></thead><tbody>' +
    D.d2.reconstruction.map(function (r) {
      return "<tr><td>" + esc(r.law) + '</td><td class="m">' + esc(r.grade) + "</td><td>" + esc(r.analyst) + "</td><td>" + mark(r.Utterance) + "</td><td>" + mark(r.Instrument) +
        "</td><td>" + mark(r.Palimpsest) + "</td><td>" + esc(r.dispute) + "</td></tr>";
    }).join("") + "</tbody></table></div>";
}

RENDER.recitation = function () {
  var host = $("#recitation");
  host.innerHTML =
    "<h2>Recitation</h2>" +
    '<p class="intro">Ch-4 is the corpus HEL carries in its mouth: nine formulae, metrically regular, recited at fixed points of field practice. The written channels show no meter at all. Either people imposed it, or Ch-4 keeps a prosody the other channels cannot record; the evidence cannot decide (A §5.8). The cola do not fall on morpheme boundaries.</p>' +
    recitationCards() +
    "<h2>Two branches, one reconstruction</h2>" +
    '<p class="intro">The formulae survive in two traditions: the Chicago notebooks, which learned from print after 1908, and the Second branch, which never did. Their differences are regular, and HEL’s comparativists reconstruct a starred Common Recitation behind both. Every change on this page happened in a human mouth or on a committee’s table; the substrate itself has no reconstructed phonology and is given none. Highlighted rows carry the p/f shibboleth.</p>' +
    d2Table() + '<div class="game" id="game"></div>' +
    "<h3 class=\"label\">Who accepts which law</h3>" + reconstructionTable() +
    "<h2>The code, 1908 to 1988</h2>" +
    '<p class="intro">The Standard itself has a history. The 1908 code was an open inventory with a coda-poor core; the Reformed List of 1988 closed it at forty-eight syllables by five ordered laws. Every 1988 form derives from its 1908 form by the laws, or is an irregular with a stated cause. In 1908 ' +
    D.d1.coda[0] + " of " + D.d1.coda[2] + " core and ritual units carried a coda anywhere; in 1988, " + D.d1.coda[1] + " of " + D.d1.coda[2] + ". The retired mnemonic strings are held in the deprecated register and are not reproduced here.</p>" +
    d1Table() +
    '<div class="stats">' + Object.keys(D.d1.irregular).map(function (k) {
      return '<div class="stat"><h3>' + esc(k) + '</h3><p class="intro">' + esc(D.d1.irregular[k][0]) + ". " + esc(D.d1.irregular[k][1]) + "</p></div>";
    }).join("") + "</div>";
  gamePick(); renderGame();
};
