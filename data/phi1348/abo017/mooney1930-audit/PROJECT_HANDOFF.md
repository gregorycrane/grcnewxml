# Mooney Suetonius handoff

Installed and locally compiled on 2026-09-07. See README.md for edition scope, counts, and unresolved issues. This is an OCR draft. Do not replace its wording with Ihm/Rolfe.

Work scripts: `work/mooney` in the current Codex workspace. Pipeline: `/Users/gcrane/github/src-persverscomp`; site: `/Users/gcrane/github/persverscomp`. Work IDs phi1348.abo017–abo022. Version IDs mooney1930-lat1, mooney1930-eng1, mooney1930-com-eng1.

Reproduction sequence: read_sources.py, extract.py, select_readings.py, align_texts.py, fix_boundaries.py, complete_anchors.py, commentary.py, prepare_notes.py, build_xml.py, mark_references.py, audit.py, validate.py. The build overwrites the output XML; later markup/audit steps must be rerun. Install via install.py with filesystem permission. Build with `python3 -m pipeline.build_all --work phi1348`, then run check_build.py. Copy updated validation and audit material to the corpus review directory. The final installed audit resides at abo017/mooney1930-audit; other lives link to it.

Remaining editorial work: review candidate lemma openings, eight unattached fragments, seven isolated English OCR words, and the two-witness disagreement inventories. Only three quotation/reference pairs are fully grouped as cit; further quotations require review. Introductory and supplementary material remains in source archives rather than the life-specific reading text. Vespasian 6.1 has no commentary, so 261 commentary passages for 262 Latin/English sections is expected.
