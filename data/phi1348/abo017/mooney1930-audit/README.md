# Mooney Suetonius, 1930 — edition inventory and review state

Prepared 7 September 2026 from the two supplied HathiTrust OCR files. This is an OCR draft, not a proofread transcription.

| Life | CTS work | Latin sections | English sections | Commentary sections | Marked lemmas |
|---|---|---:|---:|---:|---:|
| Galba | phi1348.abo017 | 49 | 49 | 49 | 486 |
| Otho | phi1348.abo018 | 28 | 28 | 28 | 285 |
| Vitellius | phi1348.abo019 | 41 | 41 | 41 | 440 |
| Vespasian | phi1348.abo020 | 57 | 57 | 56 | 554 |
| Titus | phi1348.abo021 | 26 | 26 | 26 | 256 |
| Domitian | phi1348.abo022 | 61 | 61 | 61 | 613 |

## What was done

- Created 18 TEI XML files: six Latin texts (`mooney1930-lat1`), six translations (`mooney1930-eng1`), and six commentaries (`mooney1930-com-eng1`). The text is Mooney's 1930 wording. No Rolfe/Gemini text was inserted.
- Aligned all 262 Latin sections and all 262 translated sections to the Ihm reference keys. English chapter starts follow explicit headings; inner section starts were reviewed by corresponding clause. The separate alignment records retain exact source offsets and decisions.
- Recovered 2,634 Latin lemma openings as `<mentioned ana="#note…">`, with linked `<note type="commentary">`, following the Sidgwick model. All commentary text survives the structural markup after logged cleanup. This does not establish that every lemma has been found or that all OCR is correct.
- Located commentary principally from printed chapter headings and section signs. Galba 10.3 and 18.3 have OCR `$ 3.` for `§ 3.`; Domitian 13.3 is located from the matching `consulatus septemdecim` lemma. The apparent `§ 1. d.` in Domitian 19 is an internal appendix reference, not a new section.
- There is no separate commentary on Vespasian 6.1: the printed commentary proceeds to §2. The XML retains an empty section container; the viewer has 261 nonempty commentary sections. No note has been invented to fill that gap.
- Compared the witnesses: 246 Latin/translation disagreement spans and 5,503 commentary disagreement spans are recorded. These include typography and page-layout differences; they are not counts of corrected errors. INU is generally clearer, especially for Greek. Twelve selected Latin/English repairs and five commentary selections use clearer PST readings, including the displaced `subinde` definition on printed page 191.
- Removed OCR word-break hyphens and known print signatures with change ledgers. Existing genuine compounds were retained where identified. Shared OCR mistakes can remain.
- Added 4,377 literal bibliographic references, 79 explicit glosses, and 3 reviewed citation/quotation pairs. Other quotation boundaries and unresolved reference expansions await review.

## What still needs review

`unattributed-notes.json` lists eight section-start fragments with no confirmed lemma attachment. Five are punctuation debris; the substantive cases are Vitellius 14.1 (`cuiusvis, cuiuslibet…`), Vitellius 15.1 (`Vitellius had been first`), and Titus 7.1 (`saevitiam`). They remain in their printed section, without relocation or invented Latin anchors.

`lemma-review.json` lists unconfirmed short colon openings. This is a candidate list: many entries are references or running quotations, not missed notes. It should not be read as a count of omitted commentary. All such text remains in the XML. The full note inventory is `notes.json`.

`reading-order-review.json` records isolated English words whose OCR placement may be wrong; these are marked `<unclear>` in the XML without guessing a new location. The witness-disagreement files also require editorial review, particularly Greek quotations, ellipses, superscripts and text displaced identically in both scans. The present alignment is section-level; lemma `corresp` does not assert an exact token offset.

## Sources and preserved material

`inu-pages.json` and `pst-pages.json` preserve the complete supplied OCR by scan page, including titlepages, preface, introduction, appendices and index. The life-specific XML covers the Latin and facing English on printed pages 52–187 and commentary on pages 189–609; introductory and supplementary material is archived rather than silently merged into life sections. `sources.json` records source paths and SHA-256 hashes.

`selected-readings.json`, `selected-commentary-readings.json`, `hyphen-repairs.json`, `additional-cleanup.json`, and layout-removal records document selections and cleanup. `validation.json` records XML parsing, unique identifiers, linked notes, source-text preservation and parser section checks. This validates the import mechanics, not every historical reading.

## Installation and verification

All 18 versions are installed under `/Users/gcrane/github/grcnewxml/data/phi1348/abo017` through `abo022`, with CTS metadata and work-registry entries. The local PMV was rebuilt successfully. All 785 nonempty compiled passages exactly match parser output, and all 43 pipeline tests passed. The complete shared audit is in `abo017/mooney1930-audit`; the other five lives contain a pointer to it.
