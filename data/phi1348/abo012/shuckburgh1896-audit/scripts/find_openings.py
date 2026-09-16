from pathlib import Path
import json,re,unicodedata
R=Path(__file__).parent;ns=json.load(open(R/'reviewed-notes.json'));refs=json.load(open(R/'reference-sections.json'))['12']
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower().replace('v','u').replace('j','i')) if c.isalpha())
outs=[]
for n in ns:
 words=set(norm(w) for r in refs[str(n['chapter'])] for w in re.findall(r'[^\W\d_]+',r['text']));s=n['text']
 for m in re.finditer(r'(?m)^([A-Za-z][A-Za-z ,.…-]{0,85}?)([.,:]\s+|\s+[‘\x27])',s):
  if m.start()<=n['lemma_start']+n['lemma_length']:continue
  ws=re.findall('[A-Za-z]+',m[1]);ws=[norm(w) for w in ws]
  if not ws or len(ws[0])<3 or ws[0] in {'the','and','for','was','non','his','cum','see','cic','tac','liv','dio','plin'}:continue
  if all(w in words for w in ws):outs.append(dict(parent=n['id'],chapter=n['chapter'],offset=m.start(),lemma=m[1],preview=s[m.start():m.start()+125].replace('\n',' ')))
(R/'opening-candidates.json').write_text(json.dumps(outs,ensure_ascii=False,indent=2))
for i,x in enumerate(outs):print(i,x['parent'],x['chapter'],x['preview'])
