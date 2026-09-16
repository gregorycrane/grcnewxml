from pathlib import Path
from lxml import etree as E
import json,re,sys
R=Path(__file__).parent;O=R.parents[1]/'outputs/Braithwaite-Vespasian';T='{http://www.tei-c.org/ns/1.0}';X='{http://www.w3.org/XML/1998/namespace}';ns={'t':T[1:-1]}
def compact(s):return re.sub(r'\s+','',s)
source=re.sub(r'(?m)^CHAPTER [IVX]+\s*\n','',(R/'commentary.txt').read_text())
for c in json.load(open(O/'review-decisions.json')):
 if c['action']=='Join page-spanning hyphen':assert c['before'] in source;source=source.replace(c['before'],c['after'],1)
notes=json.load(open(R/'edition-notes.json'));assert compact(''.join(n['text'] for n in notes))==compact(source)
t=E.parse(str(next(O.glob('*com-eng1.xml'))));ids=t.xpath('//@xml:id');assert len(ids)==len(set(ids));lookup={n['id']:n for n in notes};seen=[]
for p in t.xpath('//t:body//t:p',namespaces=ns):
 i=p.get(X+'id')[:-2];n=lookup[i];assert compact(''.join(p.itertext()))==compact(n['text']),i;d=p.getparent();assert d.get('n')==(n['section'] or '1');assert int(d.getparent().get('n'))==n['chapter']
 if n['lemma']:
  m=p.find(T+'mentioned');assert m.get('ana')=='#'+i;assert ''.join(m.itertext())==n['lemma'];assert p.find(T+'note').get(X+'id')==i
 seen.append(i)
assert set(seen)==set(lookup);refs=json.load(open(R/'reference-sections.json'));keys={f'{ch}.{r["sec"]}' for ch,rs in refs.items() for r in rs};actual={str(n['chapter'])+'.'+(n['section'] or '1') for n in notes};assert actual<=keys
sys.path.insert(0,'/Users/gcrane/github/src-persverscomp');from pipeline.parsers.hierarchical import parse_hierarchical_tei
parsed=parse_hierarchical_tei(str(next(O.glob('*com-eng1.xml'))),include_nonparagraph_blocks=True);pk={f'{ch}.{sec}' for b in parsed.values() for ch,ss in b.items() for sec in ss};assert pk==actual
report=dict(xml_valid=True,source_text_conservation=True,printed_sections_and_latin_reference_keys_valid=True,chapters=25,reference_sections=len(keys),commentary_sections=len(actual),sections_without_notes=sorted(keys-actual),paragraphs=len(notes),lemmas=len(t.findall('.//'+T+'mentioned')),bibl=len(t.findall('.//'+T+'bibl')),gloss=len(t.findall('.//'+T+'gloss')),cit=len(t.findall('.//'+T+'cit')),parser_matches=True);(O/'validation.json').write_text(json.dumps(report,indent=2));print(report)
