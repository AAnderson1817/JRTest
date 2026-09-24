/* Findings: contradictions the engine found in the documents, and where the build
   was wrong about itself. None was fixed silently. */
RENDER.findings = function () {
  var host = $("#findings"), L = D.findings || [];
  var n = function (k) { return L.filter(function (f) { return f.kind === k; }).length; };
  var card = function (f) {
    var tag = f.kind === "self" ? " · this build, corrected" : f.kind === "withdrawn" ? " · withdrawn: calibration" : " · repaired in the text";
    return '<div class="finding' + (f.kind === "self" ? " self" : f.kind === "withdrawn" ? " withdrawn" : "") + '"><div class="where">' + esc(f.id) + " · " + esc(f.where) + tag + "</div>" +
      "<h3>" + esc(f.title) + "</h3>" +
      (f.says ? "<p><b>The text:</b> " + esc(f.says) + "</p>" : "") +
      (f.finds ? "<p><b>The engine:</b> " + esc(f.finds) + "</p>" : "") +
      (f.repair ? '<p class="fix"><b>Repair:</b> ' + esc(f.repair) + "</p>" : "") + "</div>";
  };
  host.innerHTML = "<h2>Findings</h2>" +
    '<p class="intro">A specification in prose can say things a working system cannot do. Running the language found ' + plural(n("doc"), "place") +
    " where the Phase 1 documents contradict themselves or state a figure their own design cannot produce, and " + plural(n("self"), "place") +
    " where this build was wrong about itself. Each is listed with its repair. The document repairs change wording and numbers; none changes a canon fact, and none resolves an Authority D question. Numbers are stable, like catalogue numbers: " +
    plural(n("withdrawn"), "finding") + " first logged as contradictions were reclassified on review as calibration differences and keep their numbers." +
    (D.findings_withheld ? " " + plural(D.findings_withheld, "finding is", "findings are") + " held author-side and not shown here, because saying what was wrong would say what the sealed key holds; the gaps in the numbering are theirs." : "") + "</p>" +
    L.filter(function (f) { return f.kind !== "withdrawn"; }).map(card).join("") +
    '<h2>Withdrawn</h2><p class="intro">Feasible under the design; this build’s production rates give a different number. They are listed in the Figures table as calibration, and the documents keep their figures.</p>' +
    L.filter(function (f) { return f.kind === "withdrawn"; }).map(card).join("");
};

/* Chronology: the Archive of works, in order. */
RENDER.chronology = function () {
  var host = $("#chronology"), ev = D.chronology;
  host.innerHTML = "<h2>Chronology</h2>" +
    '<p class="intro">HEL’s own record, in order: every dated event the A-family cites, and — highlighted — the events this build adds. Nothing here comes from the rejected architectures; an earlier table that mixed five of theirs in has been corrected.</p>' +
    '<div class="tbl-wrap"><table><thead><tr><th>Year</th><th>Event</th><th>Source</th></tr></thead><tbody>' +
    ev.map(function (e) {
      return "<tr" + (e["new"] ? ' class="new"' : "") + '><td class="y">' + esc(e.year == null ? "—" : e.year) + "</td><td>" + esc(e.event) + (e["new"] ? ' <span class="badge s3">new</span>' : "") +
        '</td><td class="m">' + esc(e.src) + "</td></tr>";
    }).join("") + "</tbody></table></div>";
};
