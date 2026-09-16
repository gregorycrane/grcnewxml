# Shuckburgh's Divus Augustus (1896): work inventory

Prepared from the supplied MDP and UC1 OCR witnesses. The titlepage identifies Evelyn S. Shuckburgh, Cambridge University Press, 1896. MDP is the base; UC1 provides comparison and selected repairs.

## Delivered

- One TEI commentary for Augustus, printed pages 1–176, with all 101 source chapters and the Ihm chapter/section scheme.
- 1,037 marked lemma/commentary units, using `<mentioned ana="#note-id">` and `<note type="commentary">`, across 239 reference sections.
- 1,765 `<bibl>`, 184 `<gloss>`, and 2 reviewed `<cit>` quotation pairs. Reference/quotation markup remains conservative and incomplete.
- Complete original OCR files and parsed page archives, including the Latin reading text, introduction, appendices, and indices. These other streams have not been registered as a new Latin edition or passage commentary.
- Reviewed separation of Latin, marginal summaries, and commentary at each page boundary, checked against both OCR copies. Commentary continues across page breaks.
- 1,166 recorded differences between OCR witnesses, **not** 1,166 corrections. Forty-two selected witness-supported repairs, plus logged line/page hyphen joins, preserve the base wording elsewhere.
- Source text conservation checked through each processing stage and against the final XML. The XML has no paraphrase, modernization, or imported text from Ihm. Ihm supplies citation targets only.

## Alignment and remaining work

Section attribution is based on printed chapter headings, Latin lemma matches and reviewed decisions. Automatic phrase matches retain `cert="medium"`; semantic review of every note is not claimed. Source spellings and variant wording are preserved. Reading the same word in a section is provisional evidence, not proof of a note's entire scope.

No independent note was identified for **28.2, 61.1 or 94.1**. These remain empty section containers rather than receiving invented commentary. This is a report of the current segmentation, not a claim that the printed book has no relevant material.

**unattributed-notes.json** lists five incomplete or incompletely segmented note openings. Candidate references are review aids, not new exact attachments. **ocr-review.json** records 54 flagged note/page cases, including mixed Greek/Cyrillic OCR, split words, illustration lettering and displaced column fragments. Some unrecognized openings may remain embedded in larger notes. Text in those cases is retained. Notes and illustration lettering have not been silently discarded to make the output appear cleaner.

The two OCRs represent copies of the same edition and share errors. Agreement is not proof of correctness. This remains an **OCR draft**, especially for Greek quotations and complicated two-column continuations.

## Review files

- `note-inventory.json`: full source note text, lemma, target and placement evidence.
- `page-stream-inventory.json`: reviewed page stream splits and second-witness checks.
- `cleanup-ledger.json`, `review-decisions.json`, `additional-lemma-review.json`, `witness-corrections.json`, `final-review-decisions.json`: transformations and decisions.
- `witness-differences.json`: all token differences between page commentary streams.
- `validation.json`: XML, conservation, target and rendering checks.
- `installed-validation.json`: installation/build and test results (written after compilation).
