from pathlib import Path
import json,re,hashlib,shutil
R=Path(__file__).parent;O=R.parents[1]/'outputs/Braithwaite-Vespasian';notes=json.load(open(R/'edition-notes.json'));val=json.load(open(O/'validation.json'));flags=[]
for n in notes:
 patterns=list(re.finditer(r'[\u0400-\u04ff]+|([^\W\d_]+)-\s+[a-z]+|\b([A-Za-z]+)\s+\1\b',n['text']))
 if patterns:flags.append(dict(note=n['id'],reference=f'{n["chapter"]}.{n["section"] or "chapter-wide"}',issue='Possible OCR corruption or duplication',snippets=[n['text'][max(0,m.start()-30):m.end()+40] for m in patterns]))
for ident,detail in [('braith.note.9','OCR gives the Asian quadragesima tax as 20 per cent.; likely damaged fraction. Preserved pending image verification.'),('braith.note.13','Cursus table and inscription transcription retain OCR order; table geometry needs image review.'),('braith.note.17','Genealogical table retains OCR text; family relationships must not be inferred from flattened layout.'),('braith.note.39','Second family tree retains flattened OCR order.'),('braith.note.67','except cept appears duplicated; preserved in this single-witness draft.'),('braith.note.103','Bullet/debris within a discontinuous lemma and beginning g duplication; printed section placement is secure but transcription requires review.'),('braith.note.118','Isolated numeral 2 at chapter 9 opening: unresolved page/layout fragment, not an attributed commentary lemma.'),('braith.note.194','obvi fragment follows neighbouring note; no speculative deletion or note attribution.'),('braith.note.156','Discontinuous lemma summa aerarii ... posset retains source OCR wording without filling omitted words.')]:flags.append(dict(note=ident,issue=detail))
unattr=[dict(note=n['id'],chapter=n['chapter'],section=n['section'],text=n['text'],status='Unresolved OCR fragment, not a lemma' if n['text'].strip()=='2' else 'Chapter-wide introduction/explanation; no individual lemma') for n in notes if not n['lemma']]
(O/'ocr-review.json').write_text(json.dumps(flags,ensure_ascii=False,indent=2));(O/'unattributed-notes.json').write_text(json.dumps(unattr,ensure_ascii=False,indent=2));src=Path('/Users/gcrane/Downloads/suet-vesp-uiug-30112023708222-1788839049.txt');shutil.copy2(src,O/src.name);shutil.copy2(R/'pages.json',O/'pages.json');shutil.copy2(R/'page-offsets.json',O/'page-inventory.json');(O/'source-hashes.json').write_text(json.dumps(dict(path=str(src),sha256=hashlib.sha256(src.read_bytes()).hexdigest()),indent=2))
(O/'README.md').write_text(f'''# Braithwaite, Divus Vespasianus (1927): inventory and review

A. W. Braithwaite, *C. Suetoni Tranquilli Divus Vespasianus*, Oxford: Clarendon Press, 1927. One supplied UIUG OCR witness (30112023708222). The preface explicitly says the Latin text and apparatus are reprinted from Ihm's *editio minor*. This addition is Braithwaite's commentary; the complete OCR, including that Latin and apparatus, introduction and indices, is retained in the archive.

## Work completed

- Imported the commentary on printed pages 19–70, retaining all 25 chapters and the printed section headings.
- Aligned to Vespasian's existing Latin work `phi1348.abo020`: 57 canonical section containers, with commentary in **56**. No note is supplied for **7.3** in the source commentary stream.
- **{val['lemmas']}** `<mentioned>` lemmas linked to `<note type="commentary">`, within {val['paragraphs']} paragraph units. Restored several full lemma phrases that automatic recognition had cut apart, and recovered additional paragraph openings.
- **{val['bibl']}** `<bibl>` references, **{val['gloss']}** explicit glosses, and **{val['cit']}** reviewed `<cit>` quotation pair. Further bibliographic/quotation markup remains possible; these counts do not claim completeness.
- Removed running page headings and logged line/page hyphen joins. No lexical replacements, modernizations, paraphrases, or text imported from another edition.
- Verified conservation of the extracted commentary through segmentation and final XML markup; every lemma links to its note and every displayed section uses the existing Latin citation scheme.
- Prepared CTS metadata, registry entry, and the targeted viewer build.

## State of the work

Section placement is supported by the printed section headings, rather than guesses from a repeated Latin word. Chapter-wide introductions are explicitly labelled: their display at a chapter's first section is not a claim of a precise lemma attachment. The four entries in `unattributed-notes.json` distinguish three introductions/explanations from one unresolved numeral fragment.

`ocr-review.json` contains **{len(flags)}** flagged cases. These include a suspicious tax fraction, broken/duplicated words, mixed Greek/Cyrillic OCR, detached debris and flattened tables. They have been retained rather than silently corrected from expectation. Single-witness agreement cannot be tested. This remains an **OCR draft**, not an image-verified edition; additional paragraph boundaries or references may still need refinement.

## Review records

`note-inventory.json` contains each complete paragraph, lemma, reference and placement evidence. `cleanup-ledger.json`, `review-decisions.json` and `additional-lemma-review.json` record transformations. `page-inventory.json` and the original/parsed OCR archive preserve page provenance. `validation.json` records XML, conservation and alignment checks; `installed-validation.json` records the completed build and pipeline tests.
''')
(O/'PROJECT_HANDOFF.md').write_text('''# Braithwaite Vespasian handoff

Read README.md and the review inventories. Source: one UIUG OCR file, 1927. Do not replace source wording with the Latin reference. Only commentary is registered; Latin, apparatus and ancillary material remain archived. Printed chapters/sections are the authority for note alignment. Three chapter-wide passages and one numeral fragment have no individual lemma. Review tax fraction, OCR debris and family/cursus table layouts against images before claiming a proofread edition.

Original workspace scripts: work/braithwaite. Processing order: prepare.py, notes.py, review.py, find_openings.py, finalize_notes.py, build_xml.py, mark_references.py, validate.py, audit.py, install.py, targeted build and check_build.py. scripts/ is an archived copy; these development scripts use workspace-relative paths and the supplied source path. pages.json is their parsed source input. Full OCR and source hash are included.
''');(O/'scripts').mkdir(exist_ok=True)
for p in R.glob('*.py'):shutil.copy2(p,O/'scripts'/p.name)
print('Review flags',len(flags),'unattributed/contextual records',len(unattr))
