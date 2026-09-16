# Peck Suetonius handoff

Four versions prepared and installed: phi1348.abo011 and abo012, peck1893-lat1 and peck1893-com-eng1. Titlepage dating, omission policy, counters, and review limits are in README.md. The source is the second edition (1893 on UIUG titlepage), copyright 1889. UC1 is the base.

Preserve all existing uncommitted repository changes. Source corpus: /Users/gcrane/github/grcnewxml/data/phi1348. Pipeline: /Users/gcrane/github/src-persverscomp. Viewer: /Users/gcrane/github/persverscomp. Shared installed audit: abo011/peck1893-audit; Augustus points to it.

Scripts are in work/peck in this workspace. Source-page JSON was extracted from the two supplied OCR files using the HathiTrust page delimiters. Subsequent sequence: extract.py, select.py, align.py, fix_alignment.py, commentary_heads.py, notes.py, review_notes.py, manual_openings.py, build_xml.py, mark_references.py, validate.py, audit.py, validate.py. Rebuilding XML requires rerunning reference markup and audit. install.py updates the two work CTS files and existing registry without replacing other versions. Targeted builds use python3 -m pipeline.build_all --work phi1348.abo011 and then abo012. Run check_build.py afterward and copy final validation into the shared audit.

Editorial work remains: proofreading, uncertain word/line order, six chapter-wide or incomplete opening entries, additional bibliographic and quotation markup, and review of provisional automatic lemma matches. Complete source wording is preserved after logged cleanup; this is not a fully proofread edition. Do not fill Peck's deliberate omissions in the reading text; the actual passages survive in the commentary and are linked by editorial gap annotations. Julius 32/35 require the documented source/reference boundary mappings.
