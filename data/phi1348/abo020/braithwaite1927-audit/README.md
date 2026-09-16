# Braithwaite, Divus Vespasianus (1927): inventory and review

A. W. Braithwaite, *C. Suetoni Tranquilli Divus Vespasianus*, Oxford: Clarendon Press, 1927. One supplied UIUG OCR witness (30112023708222). The preface explicitly says the Latin text and apparatus are reprinted from Ihm's *editio minor*. This addition is Braithwaite's commentary; the complete OCR, including that Latin and apparatus, introduction and indices, is retained in the archive.

## Work completed

- Imported the commentary on printed pages 19–70, retaining all 25 chapters and the printed section headings.
- Aligned to Vespasian's existing Latin work `phi1348.abo020`: 57 canonical section containers, with commentary in **56**. No note is supplied for **7.3** in the source commentary stream.
- **217** `<mentioned>` lemmas linked to `<note type="commentary">`, within 221 paragraph units. Restored several full lemma phrases that automatic recognition had cut apart, and recovered additional paragraph openings.
- **328** `<bibl>` references, **7** explicit glosses, and **1** reviewed `<cit>` quotation pair. Further bibliographic/quotation markup remains possible; these counts do not claim completeness.
- Removed running page headings and logged line/page hyphen joins. No lexical replacements, modernizations, paraphrases, or text imported from another edition.
- Verified conservation of the extracted commentary through segmentation and final XML markup; every lemma links to its note and every displayed section uses the existing Latin citation scheme.
- Prepared CTS metadata, registry entry, and the targeted viewer build.

## State of the work

Section placement is supported by the printed section headings, rather than guesses from a repeated Latin word. Chapter-wide introductions are explicitly labelled: their display at a chapter's first section is not a claim of a precise lemma attachment. The four entries in `unattributed-notes.json` distinguish three introductions/explanations from one unresolved numeral fragment.

`ocr-review.json` contains **11** flagged cases. These include a suspicious tax fraction, broken/duplicated words, mixed Greek/Cyrillic OCR, detached debris and flattened tables. They have been retained rather than silently corrected from expectation. Single-witness agreement cannot be tested. This remains an **OCR draft**, not an image-verified edition; additional paragraph boundaries or references may still need refinement.

## Review records

`note-inventory.json` contains each complete paragraph, lemma, reference and placement evidence. `cleanup-ledger.json`, `review-decisions.json` and `additional-lemma-review.json` record transformations. `page-inventory.json` and the original/parsed OCR archive preserve page provenance. `validation.json` records XML, conservation and alignment checks; `installed-validation.json` records the completed build and pipeline tests.
