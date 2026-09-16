from pathlib import Path
from lxml import etree as E
import json,re,shutil
R=Path(__file__).parent;O=R.parents[1]/'outputs/Braithwaite-Vespasian';ns=json.load(open(R/'edition-notes.json'));refs=json.load(open(R/'reference-sections.json'));T='{http://www.tei-c.org/ns/1.0}';X='{http://www.w3.org/XML/1998/namespace}';work='phi1348.abo020';v='braithwaite1927-com-eng1'
def sub(p,tag,text=None,**a):e=E.SubElement(p,T+tag,**a);e.text=text;return e
root=E.Element(T+'TEI',nsmap={None:T[1:-1]});h=sub(root,'teiHeader');fd=sub(h,'fileDesc');ts=sub(fd,'titleStmt');sub(ts,'title','Divus Vespasianus: Braithwaite commentary (1927; OCR draft)');sub(ts,'author','Suetonius');sub(ts,'editor','A. W. Braithwaite');resp=sub(ts,'respStmt');resp.set(X+'id','ocr-editor');sub(resp,'resp','OCR collation, lemma markup, and chapter/section alignment');sub(resp,'name','Digital edition preparation');pub=sub(fd,'publicationStmt');sub(pub,'p','Local Perseus Multitext edition; see accompanying braithwaite1927-audit.');sd=sub(fd,'sourceDesc');bib=sub(sd,'bibl');sub(bib,'title','C. Suetoni Tranquilli Divus Vespasianus');sub(bib,'editor','A. W. Braithwaite');sub(bib,'publisher','Clarendon Press');sub(bib,'pubPlace','Oxford');sub(bib,'date','1927',when='1927')
sub(bib,'ref','UIUG OCR witness',target='https://hdl.handle.net/2027/uiug.30112023708222');sub(bib,'note',"Braithwaite states in his preface that the Latin text and apparatus reproduce Ihm's editio minor. This file contains Braithwaite's commentary.")
enc=sub(h,'encodingDesc');sub(enc,'p',"Single supplied UIUG OCR witness. Commentary from printed pages 19–70. Printed chapter and section headings determine citation alignment with Ihm; no second OCR witness is available. The complete original OCR including Latin text, apparatus, introduction and indices is archived. Lemmas use mentioned linked to commentary notes; source wording is retained. Logged line/page hyphen joins repair line wrapping. No conjectural lexical corrections. Chapter-wide introductions are labelled without asserting an exact section target. Incomplete OCR, suspicious duplication, figures and table layout remain in the review inventory. This is an OCR draft.");ref=sub(enc,'refsDecl',n='CTS');pat=sub(ref,'cRefPattern',n='chapter-section',matchPattern=r'(\d+)\.(\d+)',replacementPattern="#xpath(/tei:TEI/tei:text/tei:body/tei:div/tei:div[@n='$1']/tei:div[@n='$2'])");sub(pat,'p','Ihm chapter and section reference scheme.');cs=sub(ref,'citeStructure',unit='chapter',match='/TEI/text/body/div/div',use='@n');sub(cs,'citeStructure',unit='section',match='div',use='@n',delim='.');rev=sub(h,'revisionDesc');sub(rev,'change','Prepared single-witness OCR commentary; retained printed citation structure and reviewed lemma segmentation, with a conservation check and unresolved-issue inventory.',when='2026-09-07');tx=sub(root,'text');tx.set(X+'lang','eng');body=sub(tx,'body');main=sub(body,'div',type='commentary',n='urn:cts:latinLit:'+work+'.'+v);sections={}
for ch,rs in refs.items():
 d=sub(main,'div',type='textpart',subtype='chapter',n=ch)
 for r in rs:sections[int(ch),r['sec']]=sub(d,'div',type='textpart',subtype='section',n=r['sec'],corresp=f'urn:cts:latinLit:{work}.perseus-lat2:{ch}.{r["sec"]}')
pageoffs=json.load(open(R/'page-offsets.json'));pages=json.load(open(R/'pages.json'));flags=[]
for n in ns:
 ch,sec=n['chapter'],n['section'] or '1';urn=f'urn:cts:latinLit:{work}.perseus-lat2:{ch}.{sec}';p=sub(sections[ch,sec],'p',corresp=urn);p.set(X+'id',n['id']+'.p');pg=next(o['page'] for o in reversed(pageoffs) if o['offset']<=n['offset']);scan=next(o['scan'] for o in pages if o['label']==str(pg));p.set('facs','https://hdl.handle.net/2027/uiug.30112023708222?urlappend=%3Bseq='+str(scan));a=n['lemma_start'];b=a+n['lemma_length'];
 if not n['lemma']:
  p.set('type','chapter-introduction' if n['text'].strip()!='2' else 'unresolved-ocr-fragment');p.set('corresp',f'urn:cts:latinLit:{work}.perseus-lat2:{ch}');p.text=n['text'];continue
 p.text=n['text'][:a];m=sub(p,'mentioned',n['text'][a:b],ana='#'+n['id'],corresp=urn,cert='medium');m.set(X+'lang','lat');note=sub(p,'note',n['text'][b:],type='commentary');note.set(X+'id',n['id'])
# Preserve the language of Greek lemmas and mixed Greek/Latin phrases.
for m in root.findall('.//'+T+'mentioned'):
 txt=m.text or ''
 if re.search(r'[\u0370-\u03ff]',txt):
  if not re.search('[A-Za-z]',txt):m.set(X+'lang','grc')
  else:
   gm=re.search(r'[\u0370-\u03ff\u1f00-\u1fff]+',txt);m.text=txt[:gm.start()];g=sub(m,'foreign',gm[0]);g.set(X+'lang','grc');g.tail=txt[gm.end():]
E.ElementTree(root).write(str(O/(work+'.'+v+'.xml')),encoding='UTF-8',xml_declaration=True,pretty_print=True)
shutil.copy2(R/'edition-notes.json',O/'note-inventory.json');print('Wrote XML',len(ns),'paragraphs',sum(bool(n['lemma']) for n in ns),'lemmas')
