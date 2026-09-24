/* Field English: the Wall, the loans, the treadmill, the shibboleths, the names. */
function wallHTML() {
  var w = D.wall;
  var body = w.lines.map(function (l) {
    if (l.k === "dir") return '<p class="dir">' + esc(l.t) + "</p>";
    if (l.k === "quote") return '<p class="quote">' + esc(l.t) + "</p>";
    if (l.k === "op") return '<p class="op">' + esc(l.t) + "</p>";
    if (l.k === "roll") return '<p class="op roll" data-roll="1">' + esc(l.t) + "</p>";
    if (l.k === "all") return '<p class="all">' + esc(l.t) + "</p>";
    return "<p>" + l.t.split("\n").map(esc).join("<br>") + "</p>";
  }).join("");
  var notes = '<details class="perf"><summary>Performance notes</summary><ul>' + w.notes.map(function (n) { return "<li>" + esc(n) + "</li>"; }).join("") + "</ul></details>";
  var branch = '<div class="toggle" role="group" aria-label="Branch for the roll">' + ["chicago", "second"].map(function (b) {
    return '<button data-roll-branch="' + b + '" aria-pressed="' + (b === "chicago" ? "true" : "false") + '">The roll as ' + (b === "chicago" ? "Chicago" : "the Second branch") + " says it</button>";
  }).join("") + "</div>";
  return '<div class="wall"><div class="label">' + esc(w.place) + "</div><h3>" + esc(w.title) + '</h3><p class="intro">' + esc(w.when) + "</p>" +
    '<div class="poem">' + body + "</div>" + branch + notes + "</div>";
}

function loanCard(l) {
  var say = l.say ? '<div class="say">field [' + esc(l.say.field) + "]" + (l.say.standard ? " · Standard [" + esc(l.say.standard) + "]" : "") + (l.say.second ? " · Second [" + esc(l.say.second) + "]" : "") + "</div>" : "";
  var src = l.source ? '<div class="src">from ' + esc(l.source.unit) + (l.source.archive ? " — " + esc(l.source.archive) : "") + (l.source.grade ? " · " + esc(l.source.grade) : "") + "</div>" : "";
  var senses = l.senses && l.senses.length ? "<ul>" + l.senses.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul>" : "";
  var first = l.first ? '<div class="src">first attested ' + esc(l.first.year) + (l.first.where ? ", " + esc(l.first.where) : "") + "</div>" : "";
  var ex = l.examples && l.examples.length ? '<div class="hist">' + l.examples.map(function (x) { return "“" + esc(x) + "”"; }).join(" ") + "</div>" : "";
  return '<div class="loan"><h3>' + esc(l.loan) + "</h3>" + say + src + senses +
    (l.history ? '<div class="hist">' + esc(l.history) + "</div>" : "") + first + ex +
    (l.proverb ? '<div class="man">Proverb: ' + esc(l.proverb) + "</div>" : "") +
    (l.manual ? '<div class="man">' + esc(l.manual) + "</div>" : "") + "</div>";
}

function treadmill() {
  var c = D.field.euphemism_cycle;
  return '<div class="tread">' + c.stages.map(function (s) {
    return '<div class="step"><span class="label">' + esc(s.years) + "</span><b>" + esc(s.form) + "</b><span>" + esc(s.note || s.fate || "") + "</span></div>";
  }).join("") + "</div>";
}

function shibTable() {
  return '<div class="tbl-wrap"><table><thead><tr><th>Feature</th><th>Chicago</th><th>1949 Standard</th><th>Second branch</th><th>Note</th></tr></thead><tbody>' +
    D.field.shibboleths.map(function (s) {
      return "<tr><td>" + esc(s.feature) + '</td><td class="m">' + esc(s.chicago || "—") + '</td><td class="m">' + esc(s.standard_1949 || "—") + '</td><td class="m">' + esc(s.second || "—") + "</td><td>" + esc(s.note || "") + "</td></tr>";
    }).join("") + "</tbody></table></div>";
}

/* the naming generator: rules, not a list (hel/field.py) */
var NP = D.naming_pools;
function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
function coin(kind) {
  if (kind === "shape") return { name: "the " + pick(NP.shapes), why: "named for a reading of the trace’s shape that has since been deprecated; kept, because the routes are catalogued under it" };
  if (kind === "find") return { name: "the " + (1880 + Math.floor(Math.random() * 140)) + " " + pick(NP.finds), why: "named for the circumstance of its finding, as the style manual prefers for anything without a reading" };
  if (kind === "interval") return { name: "the " + pick(NP.intervals), why: "named for an interval a crew spent there; it outlives the crew and the interval" };
  return { name: pick(NP.quiet) + " " + pick(NP.numbers), why: "a cover term: deliberately mundane, assigned after a failure so that the failure has a name that says nothing" };
}
function namingHTML() {
  return '<div class="stats">' + D.field.naming.rules.map(function (r) {
    return '<div class="stat"><h3>' + esc(r.example) + '</h3><p class="intro">' + esc(r.rule) + (r.note ? ". " + esc(r.note) : "") + "</p></div>";
  }).join("") + "</div>" +
    '<div class="game"><div class="label">Coin a name</div><div class="btns">' +
    [["shape", "from a trace’s shape"], ["find", "from a find"], ["interval", "from an interval"], ["failure", "after a failure"]].map(function (k) {
      return '<button class="btn" data-coin="' + k[0] + '">' + esc(k[1]) + "</button>";
    }).join("") + '</div><div id="coined" class="coined"></div><p class="intro">Never: ' + D.field.naming.forbidden.map(esc).join("; ") + ".</p></div>";
}

RENDER.field = function () {
  var host = $("#field"), F = D.field;
  host.innerHTML = "<h2>Field English</h2>" +
    '<p class="intro">The one place in the design with a speech community — a human one. Crews call it <i>' + esc(F.crews_call_it) + "</i>; the style manual calls it " + esc(F.style_manual_calls_it) +
    ". It carries substrate units as loanwords, and because people speak it, it drifts, jokes, grieves and keeps its shibboleths. None of it is evidence about the substrate or where it came from.</p>" +
    wallHTML() +
    "<h2>Loans</h2>" + '<p class="intro">Every loan names its source unit, the Archive’s gloss and grade, what crews made of it and when, and what the style manual says about that. Loans are spelled without apostrophes, inflected or not: kalsiraed, never kalsira’d.</p>' +
    '<div class="loans">' + F.loans.map(loanCard).join("") + "</div>" +
    "<h2>The treadmill</h2>" + '<p class="intro">What crews say instead of ' + esc(F.euphemism_cycle.target) + ". Each replacement became as marked as the word it replaced.</p>" + treadmill() +
    "<h2>Shibboleths</h2>" + shibTable() +
    "<h2>Proverbs</h2>" + '<ul class="proverbs">' + F.proverbs.map(function (p) { return "<li>" + esc(p) + "</li>"; }).join("") + "</ul>" +
    "<h2>Names</h2>" + '<p class="intro">Archival names are generated by rule, and the rule is what makes a name unrenameable once routes are catalogued under it.</p>' + namingHTML();
  host.addEventListener("click", function (ev) {
    var c = ev.target.closest("[data-coin]");
    if (c) {
      var n = coin(c.getAttribute("data-coin"));
      $("#coined").innerHTML = "<b>" + esc(n.name) + "</b><span>" + esc(n.why) + "</span>";
      return;
    }
    var r = ev.target.closest("[data-roll-branch]");
    if (r) {
      var b = r.getAttribute("data-roll-branch");
      $$("[data-roll-branch]", host).forEach(function (x) { x.setAttribute("aria-pressed", x === r ? "true" : "false"); });
      var roll = D.formulae.filter(function (f) { return f.id === "roll"; })[0];
      $$("[data-roll]", host).forEach(function (p) { p.textContent = roll[b].replace(/ · ˈfɔɹti ˈwʌn$/, " ·"); });
    }
  });
  var roll = D.formulae.filter(function (f) { return f.id === "roll"; })[0];
  if (roll) $$("[data-roll]", host).forEach(function (p) { p.textContent = roll.chicago.replace(/ · ˈfɔɹti ˈwʌn$/, " ·"); });
};
