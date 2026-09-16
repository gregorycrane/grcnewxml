from pathlib import Path
from lxml import etree as E
import json,re,shutil,hashlib
R=Path(__file__).parent;O=R.parents[1]/'outputs/Braithwaite-Vespasian';pages=json.load(open(R/'pages.json'));ledger=[];s='';offsets=[]
for p in pages:
 if not p['label'].isdigit() or not 19<=int(p['label'])<=70:continue
 n=int(p['label']);ls=p['text'].splitlines();raw=ls[:]
 if n==19:
  assert ls[0]=='NOTES';ls=ls[1:]
 else:
  assert ls[0]==str(n) or ls[1]==str(n),(n,ls[:3]);ls=ls[2:]
 text='\n'.join(ls);text=re.sub(r'\n(?:C2|[A-F][2-4]?)\s*$','',text)
 for m in re.finditer(r'([^\W\d_]+)-\n([a-z]+)',text):ledger.append(dict(page=n,before=m[0],after=m[1]+m[2],reason='Line-wrap hyphen'))
 text=re.sub(r'([^\W\d_]+)-\n([a-z]+)',r'\1\2',text);offsets.append(dict(page=n,scan=p['scan'],offset=len(s)));s+=text+'\n'
(R/'commentary.txt').write_text(s);(R/'page-offsets.json').write_text(json.dumps(offsets,indent=2));(O/'cleanup-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2));t=E.parse('/Users/gcrane/github/canonical-latinLit/data/phi1348/abo020/phi1348.abo020.perseus-lat2.xml');ns={'t':'http://www.tei-c.org/ns/1.0'};refs={}
for sec in t.xpath('//t:div[@subtype="section"]',namespaces=ns):
 for note in sec.xpath('.//t:note',namespaces=ns):
  tail=note.tail or '';prev=note.getprevious();par=note.getparent()
  if prev is None:par.text=(par.text or '')+tail
  else:prev.tail=(prev.tail or '')+tail
  par.remove(note)
 refs.setdefault(sec.getparent().get('n'),[]).append(dict(sec=sec.get('n'),text=''.join(sec.itertext())))
(R/'reference-sections.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2))
for m in re.finditer(r'(?m)^CHAPTER.*|^§.*|^\$.*',s):print(m[0][:140])
print('Reference chapters',len(refs),'sections',sum(map(len,refs.values())))
