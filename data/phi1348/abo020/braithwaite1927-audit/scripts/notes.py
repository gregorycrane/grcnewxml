from pathlib import Path
import re,json,unicodedata
R=Path(__file__).parent;s=(R/'commentary.txt').read_text();refs=json.load(open(R/'reference-sections.json'))
def roman(s):
 d={'I':1,'V':5,'X':10};v=0
 for i,c in enumerate(s):v+= -d[c] if i+1<len(s) and d[c]<d[s[i+1]] else d[c]
 return v
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower().replace('v','u').replace('j','i')) if c.isalpha())
def toks(s):return [(norm(m[0]),m.start(),m.end()) for m in re.finditer(r'[^\W\d_]+',s)]
heads=list(re.finditer(r'(?m)^CHAPTER ([IVX]+)\s*\n',s));assert [roman(h[1]) for h in heads]==list(range(1,26));blocks=[];notes=[]
for hi,h in enumerate(heads):
 ch=roman(h[1]);start=h.end();end=heads[hi+1].start() if hi+1<len(heads) else len(s);part=s[start:end];sh=list(re.finditer(r'(?m)^§\s*(\d+)\.\s*',part));cuts=[(int(m[1]),m.start(),m.end()) for m in sh]
 if not cuts or cuts[0][1]>0:cuts.insert(0,(None if len(refs[str(ch)])>1 else 1,0,0))
 for j,(sec,a,lemma_start) in enumerate(cuts):
  text=part[a:cuts[j+1][1] if j+1<len(cuts) else len(part)];off=start+a;ws=toks(text);lookup={}
  for r in refs[str(ch)]:
   if sec is not None and r['sec']!=str(sec):continue
   ts=[x[0] for x in toks(r['text'])]
   for k,w in enumerate(ts):lookup.setdefault(w,[]).append((r['sec'],ts,k))
  candidates=[];forbidden=set('the and for this that was his with from have were been not there one are him all see tac dio cic liv suet cil cf'.split())
  for i,(w,a,b) in enumerate(ws):
   if w not in lookup or w in forbidden:continue
   pre=text[max(0,a-8):a];line=a==0 or '\n' in pre and not pre.rsplit('\n',1)[1].strip();isfirst=a<8;punct=bool(re.search(r'\.\s+$',pre))
   if not (line or isfirst or punct):continue
   possibilities=[]
   for _,ts,k in lookup[w]:
    endw=b;z=1;kk=k
    while z<=19:
     tail=text[endw:endw+75];nxt=ws[i+z][0] if i+z<len(ws) else ''
     # A lemma is followed by defining punctuation or recognizably English prose.
     if (z>1 or len(w)>2) and (re.match(r'[:.,]\s*(?:[A-Z‘“\x27\"]|i\.?\s*e\.|e\.?\s*g\.|used|see|cf\.|i.e.|was|is|for|the|a\b|an\b|in\b|of\b|on\b|so\b|only|about|at\b|by\b|before|with|without|his|from|sensu)',tail) or re.match(r'\s+(?:was|is|were|means|refers|are|seems)\b',tail)):
      possibilities.append((z,endw))
     if i+z>=len(ws) or kk+1>=len(ts):break
     gap=text[endw:ws[i+z][1]];nw=ws[i+z][0]
     if len(gap)>12 or re.search(r'[^.\s…—–-]',gap):break
     if ts[kk+1]==nw:kk+=1
     elif '..' in gap or '…' in gap:
      hits=[k2 for k2 in range(kk+1,len(ts)) if ts[k2]==nw]
      if not hits:break
      kk=hits[0]
     else:break
     endw=ws[i+z][2];z+=1
   if possibilities:
    _,b=max(possibilities);candidates.append(dict(a=a,b=b,lemma=text[a:b]))
  selected=[]
  for c in candidates:
   if not selected or c['a']>=selected[-1]['b']:selected.append(c)
  if selected and re.fullmatch(r'\s*§\s*\d+\.\s*',text[:selected[0]['a']]):selected[0]['prefix']=0
  elif not selected or selected[0]['a']>0:selected.insert(0,dict(a=0,b=0,lemma=None))
  for k,c in enumerate(selected):
   a=c.get('prefix',c['a']);end=selected[k+1].get('prefix',selected[k+1]['a']) if k+1<len(selected) else len(text);txt=text[a:end]
   if not txt.strip():continue
   notes.append(dict(id=f'braith.note.{len(notes)+1}',chapter=ch,section=str(sec) if sec else None,lemma=c['lemma'],lemma_start=c['a']-a,lemma_length=c['b']-c['a'],text=txt,offset=off+a,evidence='Printed chapter/section heading' if sec else 'Chapter-wide introduction; no section attribution'))
body=re.sub(r'(?m)^CHAPTER [IVX]+\s*\n','',s);assert re.sub(r'\s+','',''.join(n['text'] for n in notes))==re.sub(r'\s+','',body)
(R/'notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
for ch in range(1,26):print(ch,'; '.join(n['id'].split('.')[-1]+':'+str(n['lemma']).replace('\n',' ')+'→'+str(n['section']) for n in notes if n['chapter']==ch))
print('Notes',len(notes),'lemmas',sum(bool(n['lemma']) for n in notes))
