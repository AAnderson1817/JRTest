"""HEL — the Horizon Expedition League substrate, as an executable system.

Everything in this package is Authority C (a recommendation awaiting approval),
exactly like the design documents it implements. The package makes three
promises the prose could not keep on its own:

1. **The grammar is a program.** Any segment can be parsed, checked, glossed and
   rendered; any claim the documents make about the grammar can be tested.
2. **The corpus is rendered, not authored** (benchmark Design rule 3). Records are
   produced from a sealed world, damaged by a stated attrition model, transcribed
   by the 1908 committee's procedure with its known errors, and only then
   catalogued. Every statistic the Archive publishes is computed from that
   catalogue.
3. **The sealed and the published never mix.** Modules that read ``sealed/`` say so
   in their docstring. The export used by anything shipped (``hel.export``) strips
   every sealed field and is checked for leaks.

Layers (brief §7) are kept visibly distinct throughout:
  layer 1 — the trace (``hel.trace``; sealed geometry, rendered by ``hel.script``)
  layer 2 — HEL scholarly transliteration (``hel.phonology``, ``hel.grammar``)
  layer 3 — HEL field pronunciation (``hel.phonology.ipa``, ``hel.diachrony``)
  layer 4 — English gloss (``hel.grammar.gloss_line``, ``hel.grammar.translate``)
"""

__version__ = "2.0.0"
