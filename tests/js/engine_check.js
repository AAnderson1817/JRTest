// The browser engine must agree with the Python engine on the worked examples.
// Run by tests/test_phase2.py when node is available; exits non-zero on disagreement.
const path = require('path');
const root = path.resolve(__dirname, '..', '..');
const HEL = require(path.join(root, 'reading_room', 'engine.js'));
const inv = require(path.join(root, 'reading_room', 'inventory.json'));
const reg = require(path.join(root, 'corpus', 'register.json')).units;
const common = require(path.join(root, 'reading_room', 'common.json'));
HEL.init(inv, reg, common);
const fail = [];
const ex = {
  ex1: "harnuli-in-ken · ke-telnuro-is-ru · ru-kalsira-in=hilun-to-pukal · tir lekur",
  ex2: "harnuli-ar-pel-sen · pe-kurhali-in=hilun-nu-hilun · hos",
  ex3: "sarkile-in-sil · si-lartuki-ol=hilun-sa-kihar · lunkani · [41]",
};
for (const [k, t] of Object.entries(ex)) {
  const s = HEL.parseSegment(t);
  if (HEL.translit(s) !== t) fail.push(k + ': round trip');
  if (!HEL.wellFormed(s, k === 'ex3' ? 'Ch-4' : 'Ch-1')) fail.push(k + ': not well-formed');
}
const s1 = HEL.parseSegment(ex.ex1);
const rb = HEL.readback(s1);
if (rb[1] !== "Harnuli, terminal, edge seven. Telnuro, medial, edge one. Kalsira, terminal. Locus open, pass later, phase measured ahead. Witnessed, recurrent.") fail.push('readback B: ' + rb[1]);
if (rb[2] !== "Confirmed, edge seven, edge one.") fail.push('readback C: ' + rb[2]);
if (!HEL.check(HEL.reverse(s1, 1)).map(f => f.code).includes('E-ANCHOR')) fail.push('reversal edit does not give E-ANCHOR');
const roll = HEL.parseSegment("inpelu-in-tul · tu-hasilnu-in=hilun-nu-nikur · lunkani · [41]");
if (HEL.recite(roll, 'second') !== "ˈinfilu-in-tul · ˈhasilnu-in=hilun-nu-nikur · ˈlunkani · ˈfɔɹti ˈwʌn") fail.push('Second-branch roll: ' + HEL.recite(roll, 'second'));
const sealing = HEL.parseSegment("nirtoka-pel-sen · pe-olsihe-in=hilun-nu-hilun · tuwalsi · [41]");
if (!HEL.recite(sealing, 'second').includes('-fil-sen')) fail.push('Second branch must keep sen (F-27): ' + HEL.recite(sealing, 'second'));
const tr = HEL.translate(s1).text;
if (!tr.startsWith("Route: HARNULI → via TELNURO → KALSIRA. ")) fail.push('translation: ' + tr);
const svg = HEL.traceSVG(s1);
if (!svg.startsWith('<svg') || svg.length < 2000) fail.push('trace SVG');
if (fail.length) { console.error(fail.join('\n')); process.exit(1); }
console.log('engine.js agrees with the Python engine');
