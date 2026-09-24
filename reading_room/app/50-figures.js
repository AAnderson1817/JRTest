/* Figures: what the Archive publishes about its own catalogue, computed, and the
   documents' own numbers checked against it. */
function bars(obj, total, cls, fmtv) {
  var keys = Object.keys(obj);
  var max = Math.max.apply(null, keys.map(function (k) { return obj[k]; }));
  return '<div class="bars">' + keys.map(function (k) {
    var v = obj[k], w = total ? v / total : v / max;
    return '<div class="bar"><span>' + esc(k) + '</span><span class="track"><span class="fill' + (typeof cls === "function" ? cls(k) : cls || "") +
      '" style="width:' + (w * 100).toFixed(1) + '%"></span></span><span class="v">' + esc(fmtv ? fmtv(v) : v) + "</span></div>";
  }).join("") + "</div>";
}
function kv(rows) {
  return '<div class="kv">' + rows.map(function (r) { return "<span>" + r[0] + "</span><span>" + esc(r[1]) + "</span>"; }).join("") + "</div>";
}
function stat(title, inner, note) {
  return '<div class="stat"><h3>' + esc(title) + "</h3>" + inner + (note ? '<p class="intro small">' + note + "</p>" : "") + "</div>";
}
function claimsTable() {
  if (!D.claims || !D.claims.length) return "";
  var label = { holds: '<span class="yes">holds</span>', repaired: '<span class="warnc">repaired</span>', calibration: '<span class="quiet">calibration</span>', fails: '<span class="no">fails</span>' };
  var counts = {};
  D.claims.forEach(function (c) { counts[c.status] = (counts[c.status] || 0) + 1; });
  return "<h2>The documents’ numbers, checked</h2>" +
    '<p class="intro">Every figure the A-family states about its catalogue, set against the catalogue on this page: ' + (counts.holds || 0) + " hold, " + (counts.repaired || 0) +
    " were repaired in the text because they contradicted the design (the correction is under Findings), and " + (counts.calibration || 0) +
    " are calibration differences — feasible figures this build's rates do not reproduce, left standing in the documents." + (counts.fails ? " " + counts.fails + " fail." : " None fails.") + "</p>" +
    '<div class="tbl-wrap"><table><thead><tr><th>Claim</th><th>Where</th><th>The document said</th><th>This corpus</th><th>Status</th></tr></thead><tbody>' +
    D.claims.map(function (c) {
      var got = typeof c.got === "object" ? JSON.stringify(c.got).replace(/[{}"]/g, "").replace(/,/g, ", ").replace(/:/g, " ") : String(c.got);
      var says = esc(c.says) + (c.now ? '<br><span class="warnc">now: ' + esc(c.now) + "</span>" : "");
      return "<tr><td>" + esc(c.what) + (c.note ? '<br><span class="quiet">' + esc(c.note) + "</span>" : "") + '</td><td class="m">' + esc(c.where) + '</td><td class="m">' + says + '</td><td class="m">' + esc(got) + "</td><td>" +
        (label[c.status] || esc(c.status)) + (c.finding ? ' <span class="m">' + esc(c.finding) + "</span>" : "") + "</td></tr>";
    }).join("") + "</tbody></table></div>";
}

RENDER.figures = function () {
  var F = D.figures.figures, T = D.figures.iii, host = $("#figures");
  var cond = { intact: 0, worn: 0, fractured: 0, eroded: 0 };
  D.entries.forEach(function (e) { if (e.channel === "Ch-1" && !e.part && e.condition in cond) cond[e.condition]++; });
  var ch1 = D.entries.filter(function (e) { return e.channel === "Ch-1" && !e.part; }).length;
  var s3 = function (k) { return /III/.test(k) ? " s3" : ""; };
  var X = D.metrics;
  var profiles = { "Stratum III units": F.profile_III.coda_final_share, "functional roots": X.root_coda_final_share, "all functional tokens": F.profile_functional.coda_final_share };
  var syl = { "Stratum III units": F.profile_III.mean_syllables, "functional roots": X.root_mean_syllables, "all functional tokens": F.profile_functional.mean_syllables };
  host.innerHTML = "<h2>Figures</h2>" +
    '<p class="intro">Everything here is computed from the catalogue on this page by the same build that made it. Rebuild with the same seed and every number comes back the same.</p>' +
    '<div class="stats">' +
    stat("The catalogue", kv([["Accessions", fmt(D.entries.length)], ["Tokens", fmt(F.tokens)], ["Registered units", fmt(D.register.length)], ["Sequences", fmt(F.sequences)],
      ["Longest sequence", F.longest_sequence + " tokens"], ["Functional segments", fmt(F.functional_segments)], ["Functional types", fmt(F.functional_types)],
      ["…of which hapax", fmt(F.functional_seq_hapax)]])) +
    stat("Channel share of tokens", bars(F.channel_share, 1, "", function (v) { return pct(v); })) +
    stat("Stratum share of tokens", bars(F.stratum_share, 1, s3, function (v) { return pct(v); })) +
    stat("Condition of Ch-1 objects", bars(cond, ch1, "", function (v) { return fmt(v); }),
      "Objects the documents count exactly (the bound pairs, the half-negated edges, the named objects) are rendered intact so the counts can be checked; the rest draw a condition from the taphonomy rates (intact .36, worn .22, fractured .32, eroded .10).") +
    stat("Two silhouettes", '<div class="label">ending in a coda</div>' + bars(profiles, 1, s3, function (v) { return pct(v, 0); }) +
      '<div class="label">syllables per unit</div>' + bars(syl, 0, s3, function (v) { return Number(v).toFixed(2); }),
      "Stratum III units are the same length as the functional roots. What differs is the ending: no functional root ends in a coda, and almost every Stratum III unit does (A-reserve §4.6, as repaired — F-02).") +
    stat("Stratum III", kv([["Sequences", T.sequences], ["Tokens", T.tokens], ["Mean length", T.mean_length], ["Length range", T.length_range.join("–")],
      ["Divisible by three", T.divisible_by_three + " of " + T.sequences], ["Types", T.types], ["Types in one sequence only", T.types_in_one_sequence],
      ["P(type recurs inside its record)", T.p_recur_within], ["P(type recurs elsewhere)", T.p_recur_elsewhere], ["Find loci", T.find_loci], ["Provisional", T.provisional]])) +
    stat("Where Stratum III is found", bars(T.position, 0, " s3") + bars(T.channel, 0, " s3")) +
    stat("Counts the documents state", kv([["kalsira-ru, all", F.kalsira_ru.total], ["…completed, Stratum I", F.kalsira_ru.completed_I], ["…frozen", F.kalsira_ru.uncompleted],
      ["lartuki-halu", F.lartuki_halu], ["Half-negated edges (tail-only -mun)", F.tail_only_mun], ["Stacked warrants", F.stacked_warrants], ["…reversed order", F.stacked_reversed],
      ["Segments ending in a broken half", F.segments_ending_in_broken_half + " (" + pct(F.broken_share) + ")"], ["SHUNT and RECUR edges", F.shunt_recur_edges],
      ["ADJ halves", F.adj_halves], ["Nodes on the junction map", F.junction_map_nodes]])) +
    stat("Imports and the Open Register", kv([["Discharge (H1, Treloar 1926)", F.imports.H1_discharge], ["Unentitled (H2, Thaxter 1957)", F.imports.H2_unent],
      ["Recurrence scope (H3, Merrow 1972)", F.imports.H3_rscope], ["Unentitled segments", F.unentitled], ["Shadow parses", F.shadow_parses], ["Open Register entries", F.open_register]])) +
    stat("The Stratum II environment", kv([["Cuts before a vowel-initial root", F.stratum_II_env.total], ["…on Ch-1 objects", F.stratum_II_env.ch1],
      ["…where the trace is short", F.stratum_II_env.ch1_short], ["…where it is indeterminate", F.stratum_II_env.ch1_undetermined],
      ["…indeterminate, older register consulted", F.stratum_II_env.ch1_undetermined_with_register]])) +
    "</div>" + claimsTable();
};
