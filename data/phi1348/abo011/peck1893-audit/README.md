# Peck, Suetonius: second edition — inventory and review state

Harry Thurston Peck, *Gai Svetoni Tranqvilli De Vita Caesarvm Libri Dvo*, New York, Henry Holt and Company, **1893, second edition**. Covers Julius Caesar and Augustus; Latin and English commentary, no English translation.

Both supplied copies print “SECOND EDITION.” The Illinois titlepage explicitly reads 1893; the California titlepage OCR omits the year. The common 1889 date is the copyright/catalogue date, not the date used for this second-edition version. Both contain references to publications through 1892. UC1 is the base because UIUG contains substantially more marginal handwriting intrusions.

## Files and alignment

- `phi1348.abo011.peck1893-lat1.xml`: Julius Caesar, 187 canonical section positions, including five wholly omitted positions marked as editorial gaps.
- `phi1348.abo012.peck1893-lat1.xml`: Augustus, 242 canonical section positions, including two wholly omitted positions marked as editorial gaps.
- Matching `peck1893-com-eng1.xml` files: 382 Julius lemmas and 373 Augustus lemmas, in 774 source-preserving paragraphs. The parser produces 162 Julius commentary passages and 195 Augustus commentary passages. Empty commentary sections are listed in validation.json; this is not a claim that the corresponding source has no relevant discussion. Some chapter-wide excerpts span multiple sections.
- Citation structure follows Ihm, including chapters and sections. Source chapter milestones retain Peck's printed scheme. Julius 32 begins later in Peck (after *Cunctanti ostentum tale factum est*); Julius 35 begins after the Egyptian-war narrative. These passages have been moved to their correct reference divisions without altering words. `chapter-boundary-adjustments.json` records the changes. The source's *Iunius Saturninus* at Augustus 27.2 is retained against Ihm's *Iulius*.
- Lemmas use `<mentioned ana="#…">` and linked `<note type="commentary">`, following the Sidgwick model. Exact-word matches are provisional and marked `cert="medium"`; manual opening reviews also recover inflected, elliptical and variant forms. Source wording is retained even where the OCR lemma is defective (e.g. *Curio*, *confiavit*). References/glosses are only a conservative first pass: 279 `bibl`, 69 `gloss`, and one reviewed `cit`/`quote` pair. No external identifiers have been invented for unresolved abbreviations.

## Peck's omissions

Peck's preface says he moved some sentences into the notes without changing the original numbering. We preserve that editorial decision. The reading text does not silently borrow missing Latin from Ihm, Butler–Cary, Rolfe, or a generated supplement.

The identified passages are Julius 7.2, the end of 22.2, all of chapter 49, Augustus 68, the continuation of 69.1 and all of 69.2, and a sentence in 71.1. Ten `gap` elements mark these omissions in the reading texts. The actual retained extracts remain in the commentary as `p type="editorially-relocated-text"`. The chapter 49 extract is displayed at 49.1 with a 49.1–49.4 range; the Augustus 69 excerpt is displayed at 69.1 with a 69.1–69.2 range. These range anchors do not pretend the whole extract belongs to one section.

## Unresolved notes and OCR

`unattributed-notes.json` lists the remaining chapter-wide or incomplete opening fragments without a precise lemma/section attachment. They are kept in their known source chapter and displayed at its first section, with chapter-level `corresp`; this display convention is not evidence for a particular section. The general manuscript discussion at Julius 1 belongs to this category. Some fragmentary opening labels still need reconstruction from the scans.

`reviewed-notes.json` contains every paragraph's source offset, lemma, target and placement evidence. Phrase matching is not full proofreading: missed paragraph starts, quoted words misidentified as lemmas, and erroneous OCR may remain. `manual-lemma-openings.json` and `lemma-decisions.json` record specific reviews. All commentary characters survive markup, apart from the separately recorded layout/word-break cleanup. No notes were discarded because their exact lemma could not be established.

`ocr-review.json` flags conspicuous non-Latin intrusions and the displaced `um-` near Julius 68–69. The latter appears displaced in both OCR copies; it is retained and marked unclear rather than moved speculatively. Other shared OCR errors may remain undetected. `unlocated-page-links.json` records notes for which an exact starting-page match could not be established; no facsimile page was guessed.

## Witnesses and reproducibility

`uc1-pages.json` and `uiug-pages.json` preserve the full supplied OCR, including introductory material and index. The reading XML covers printed Latin pp. 1–113; commentary pp. 115–208. Page 114 abbreviations and the introduction/index remain in the source archive. California scan 92 is correctly identified as printed p. 48 despite its erroneous OCR page label; scans 93–94 are a plate and blank, not replacement text pages.

`sources.json` gives original paths, HathiTrust identifiers and SHA-256 hashes. `witness-differences.json` records 1,125 disagreement spans across text and commentary, including layout noise; these are not 1,125 corrected errors. `hyphen-cleanup.json`, `layout-removals.json`, and `selected-readings-and-cleanup.json` record transformations and selections. `reference-differences.json` is the initial chapter-local comparison with Ihm; read it together with chapter-boundary-adjustments.json because initial 31/32 and 34/35 boundary differences were subsequently resolved.

Validation checks XML parsing, unique identifiers, linked notes, canonical section keys, and source-character preservation. Those checks validate the conversion, not every historical or OCR reading. Reproduction scripts are in the current workspace's `work/peck` directory.

## Installed and compiled

The four XML files and CTS records are installed under the two work directories, with existing registry entries preserved. Both targeted local viewer builds succeeded. All 786 compiled passages (429 Latin positions including labelled gaps, 357 commentary passages) match the XML parser output exactly; all 755 lemmas render with the project lemma styling. All 43 pipeline tests passed. No remote publication or Git commit was performed.
