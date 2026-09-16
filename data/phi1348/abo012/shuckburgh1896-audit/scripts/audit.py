from pathlib import Path
import json,re,hashlib,shutil
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';ns=json.load(open(R/'edition-notes.json'));val=json.load(open(O/'validation.json'));ps=json.load(open(R/'page-offsets.json'));issues=[]
for n in ns:
 bad=list(re.finditer(r'[\u0400-\u04ff]+|[^\W\d_]+-\s+[a-z]+|\b\w+_\w+\b',n['text']))
 if bad:issues.append(dict(note=n['id'],reference=f'{n["chapter"]}.{n["section"]}',issue='Possible OCR corruption or unresolved broken word',snippets=[n['text'][max(0,m.start()-30):m.end()+45] for m in bad]))
manual=[(33,'Truncated and displaced words around inter Mylas et Naulochum; remaining Pom-/peius and isolated numeral need image review.'),(45,'Damaged per-/persons passage; two OCRs differ in text order.'),(66,'Two-column continuation order: latter extending perhaps ... appears after the next column; retained without speculative rearrangement.'),(79,'Marginal summary The Senate occurs within the opening commentary sentence; not silently removed.'),(120,'Coin illustration lettering mixed with commentary. Retained pending image review.'),(135,'Setalis / condly split across commentary text: likely displaced Secondly; no speculative reordering.'),(145,'con- before residua diurni actus and ficeret after its gloss: displaced lemma fragment.'),(146,'Coin illustration lettering CAEST remains in OCR commentary stream.'),(153,'Displaced archa-/isms and Maecenatem lemma; source order needs page-image review.')]
for page,detail in manual:issues.append(dict(page=page,issue=detail))
(O/'ocr-review.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2))
unattr=[dict(page=26,source='alios, patrem et filium...',issue='Incomplete lemma/quotation continuation; opening marked but exact extent needs review',parent='shuck.extra.16',candidate_reference='13.2'),dict(page=25,source='exercitus. ceterosque duces et',issue='OCR word order obscures full lemma; retained inside existing commentary rather than silently reconstructed',candidate_reference='12.1'),dict(page=135,source='Setalis ... condly',issue='Lemma talis is embedded in displaced prose; not separately anchored',candidate_reference='71.2'),dict(page=145,source='con- ... ficeret',issue='Displaced lemma fragment remains with neighbouring commentary; no separate exact lemma anchor',candidate_reference='78.1'),dict(page=153,source='Maecenatem...myrobrechis ... cincinnos',issue='Opening remains embedded alongside displaced column text; needs image review for a clean separate note',candidate_reference='86.2')]
(O/'unattributed-notes.json').write_text(json.dumps(unattr,ensure_ascii=False,indent=2))
hashes={}
for k,name in [('mdp','suet-shuck-mdp-39015028728833-1788838342.txt'),('uc1','suet-shuck-uc1-31158008883992-1788838412.txt')]:
 p=Path('/Users/gcrane/Downloads')/name;hashes[k]=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest());shutil.copy2(p,O/name)
(O/'source-hashes.json').write_text(json.dumps(hashes,indent=2))
report=f'''# Shuckburgh's Divus Augustus (1896): work inventory

Prepared from the supplied MDP and UC1 OCR witnesses. The titlepage identifies Evelyn S. Shuckburgh, Cambridge University Press, 1896. MDP is the base; UC1 provides comparison and selected repairs.

## Delivered

- One TEI commentary for Augustus, printed pages 1–176, with all 101 source chapters and the Ihm chapter/section scheme.
- {val['lemmas']:,} marked lemma/commentary units, using `<mentioned ana="#note-id">` and `<note type="commentary">`, across {val['commentary_sections']} reference sections.
- {val['bibl']:,} `<bibl>`, {val['gloss']} `<gloss>`, and {val['cit']} reviewed `<cit>` quotation pairs. Reference/quotation markup remains conservative and incomplete.
- Complete original OCR files and parsed page archives, including the Latin reading text, introduction, appendices, and indices. These other streams have not been registered as a new Latin edition or passage commentary.
- Reviewed separation of Latin, marginal summaries, and commentary at each page boundary, checked against both OCR copies. Commentary continues across page breaks.
- 1,166 recorded differences between OCR witnesses, **not** 1,166 corrections. Forty-two selected witness-supported repairs, plus logged line/page hyphen joins, preserve the base wording elsewhere.
- Source text conservation checked through each processing stage and against the final XML. The XML has no paraphrase, modernization, or imported text from Ihm. Ihm supplies citation targets only.

## Alignment and remaining work

Section attribution is based on printed chapter headings, Latin lemma matches and reviewed decisions. Automatic phrase matches retain `cert="medium"`; semantic review of every note is not claimed. Source spellings and variant wording are preserved. Reading the same word in a section is provisional evidence, not proof of a note's entire scope.

No independent note was identified for **28.2, 61.1 or 94.1**. These remain empty section containers rather than receiving invented commentary. This is a report of the current segmentation, not a claim that the printed book has no relevant material.

**unattributed-notes.json** lists five incomplete or incompletely segmented note openings. Candidate references are review aids, not new exact attachments. **ocr-review.json** records {len(issues)} flagged note/page cases, including mixed Greek/Cyrillic OCR, split words, illustration lettering and displaced column fragments. Some unrecognized openings may remain embedded in larger notes. Text in those cases is retained. Notes and illustration lettering have not been silently discarded to make the output appear cleaner.

The two OCRs represent copies of the same edition and share errors. Agreement is not proof of correctness. This remains an **OCR draft**, especially for Greek quotations and complicated two-column continuations.

## Review files

- `note-inventory.json`: full source note text, lemma, target and placement evidence.
- `page-stream-inventory.json`: reviewed page stream splits and second-witness checks.
- `cleanup-ledger.json`, `review-decisions.json`, `additional-lemma-review.json`, `witness-corrections.json`, `final-review-decisions.json`: transformations and decisions.
- `witness-differences.json`: all token differences between page commentary streams.
- `validation.json`: XML, conservation, target and rendering checks.
- `installed-validation.json`: installation/build and test results (written after compilation).
'''
(O/'README.md').write_text(report)
(O/'PROJECT_HANDOFF.md').write_text('''# Shuckburgh Augustus handoff

Read README.md and the JSON review inventories first. Preserve existing corpus/pipeline work. Only the commentary has been installed; the complete Latin and ancillary OCR are archived for future processing.

Reproduction scripts are in `scripts/`; their original workspace is `work/shuckburgh`. Processing order: split.py, extract.py, prepare_notes.py, notes.py, review.py, find_openings.py, add_openings.py, correct.py, final_review.py, build_xml.py, mark_references.py, validate.py, audit.py. The original parsed witness page JSON files are needed beside the scripts. Scripts use workspace-relative paths and are development tools, not a standalone relocatable package. The original two OCR files and source hashes are included.

Before treating this edition as proofread, resolve the five incomplete note openings, review Greek OCR against images, inspect displaced column text, and verify provisional section targets. Never replace source wording with the reference Latin to improve an alignment score.
''')
(O/'scripts').mkdir(exist_ok=True)
for p in R.glob('*.py'):shutil.copy2(p,O/'scripts'/p.name)
print('Audit cases',len(issues),'incomplete openings',len(unattr))
