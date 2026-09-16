from pathlib import Path
from lxml import etree as E
import re,json,sys,hashlib,difflib
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';T='{http://www.tei-c.org/ns/1.0}';X='{http://www.w3.org/XML/1998/namespace}';ns={'t':T[1:-1]}
def compact(s):return re.sub(r'\s+','',s)
def join(name):return ''.join(n['text'] for n in json.load(open(R/name)))
source=(R/'selected-com-12.txt').read_text();assert compact(join('notes.json'))==compact(source)
expected=source
for c in json.load(open(O/'review-decisions.json')):
 if c['action']=='Join page-spanning broken word':
  assert c['before'] in expected;expected=expected.replace(c['before'],c['after'],1)
assert compact(join('reviewed-notes.json'))==compact(expected)
assert compact(join('reviewed-notes.json'))==compact(join('final-notes.json'))
before=json.load(open(R/'final-notes.json'));repairs=json.load(open(O/'witness-corrections.json'))
for c in repairs:
 n=next(n for n in before if n['id']==c['note']);assert c['before'] in n['text'];n['text']=n['text'].replace(c['before'],c['after'],1)
assert compact(''.join(n['text'] for n in before))==compact(join('corrected-notes.json'))
assert compact(join('edition-notes.json'))==compact(join('corrected-notes.json').replace('er Mylas et Naulochum','inter Mylas et Naulochum'))
notes=json.load(open(R/'edition-notes.json'));path=next(O.glob('*com-eng1.xml'));tree=E.parse(str(path));ids=tree.xpath('//@xml:id');assert len(ids)==len(set(ids));lookup={n['id']:n for n in notes};seen=[]
for p in tree.xpath('//t:body//t:p',namespaces=ns):
 i=p.get(X+'id')[:-2];n=lookup[i];assert compact(''.join(p.itertext()))==compact(n['text']),i
 m=p.find(T+'mentioned');assert m.get('ana')=='#'+i;assert p.find(T+'note').get(X+'id')==i;assert ''.join(m.itertext())==n['lemma'];sec=p.getparent();assert sec.get('n')==n['section'];assert int(sec.getparent().get('n'))==n['chapter'];seen.append(i)
assert set(seen)==set(lookup)
refs=json.load(open(R/'reference-sections.json'))['12'];keys={f'{ch}.{r["sec"]}' for ch,rs in refs.items() for r in rs};actual={f'{n["chapter"]}.{n["section"]}' for n in notes}
sys.path.insert(0,'/Users/gcrane/github/src-persverscomp');from pipeline.parsers.hierarchical import parse_hierarchical_tei
parsed=parse_hierarchical_tei(str(path),include_nonparagraph_blocks=True);parsedkeys={f'{ch}.{sec}' for book in parsed.values() for ch,secs in book.items() for sec in secs};assert parsedkeys==actual,(parsedkeys-actual,actual-parsedkeys)
report=dict(xml_valid=True,ids_and_lemma_links_valid=True,source_text_preserved_except_logged_repairs=True,chapters=101,reference_sections=len(keys),commentary_sections=len(actual),sections_without_identified_notes=sorted(keys-actual,key=lambda x:tuple(map(int,x.split('.')))),notes=len(notes),lemmas=len(notes),bibl=len(tree.findall('.//'+T+'bibl')),gloss=len(tree.findall('.//'+T+'gloss')),cit=len(tree.findall('.//'+T+'cit')),parser_sections_match=True)
(O/'validation.json').write_text(json.dumps(report,indent=2));print(report)
