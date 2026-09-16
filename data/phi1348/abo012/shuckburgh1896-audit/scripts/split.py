from pathlib import Path
import json,re,difflib,unicodedata
R=Path(__file__).parent
ref=json.load(open(R.parent/'peck/reference-sections.json'))['12'];(R/'reference-sections.json').write_text(json.dumps({'12':ref},ensure_ascii=False))
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower().replace('v','u').replace('j','i')) if c.isalpha())
def toks(s):return [(norm(m[0]),m.start(),m.end()) for m in re.finditer(r'[^\W\d_]+',s)]
a=[];chap=[]
for ch,rs in ref.items():
 for r in rs:
  w=toks(r['text']);a.extend(x[0] for x in w);chap.extend([int(ch)]*len(w))
rows=[]
for p in json.load(open(R/'mdp-pages.json')):
 if not p['label'].isdigit() or not 1<=int(p['label'])<=177:continue
 n=int(p['label']);s=p['text'];ts=toks(s);b=[x[0] for x in ts];blocks=difflib.SequenceMatcher(None,a,b[:600],autojunk=False).get_matching_blocks();bb=[x for x in blocks if x.size>=4 and x.b<95]
 if not bb:print('NONE',n);continue
 first=bb[0];chosen=[first];last=first
 for x in blocks:
  if x.b<=first.b:continue
  if x.b-(last.b+last.size)>9 or x.a-(last.a+last.size)>7:break
  if x.size>=2:chosen.append(x);last=x
 end=ts[last.b+last.size-1][2];line=s.count('\n',0,end);lines=s.splitlines();rows.append(dict(page=n,scan=p['scan'],split=line+1,ch=chap[first.a],latin_start=lines[:5],last=lines[max(0,line-1):line+1],first=lines[line+1:line+4]))
(R/'split-proposals.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for r in rows:print(r['page'],r['ch'],r['split'],' | '.join(r['last']),' >>> ',' | '.join(r['first']))
