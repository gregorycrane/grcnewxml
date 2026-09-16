from pathlib import Path
import json,re,unicodedata
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';refs=json.load(open(R/'reference-sections.json'))['12'];s=(R/'selected-com-12.txt').read_text();heads=[]
for h in json.load(open(R/'head-candidates.json')):
 if h['ch'] not in [x['ch'] for x in heads] and (not heads or h['ch']>heads[-1]['ch']):heads.append(h)
a=s.index('curam...alvei Tiberis.');heads.append(dict(ch=37,offset=a,end=a,page=83,preview=s[a:a+100],evidence='Chapter number 37 displaced above preceding note continuation on page 83; lemma identifies chapter 37'))
heads.sort(key=lambda x:x['offset']);assert [h['ch'] for h in heads]==list(range(1,102))
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower().replace('v','u').replace('j','i')) if c.isalpha())
def tokens(s):return [(norm(m[0]),m.start(),m.end()) for m in re.finditer(r'[^\W\d_]+',s)]
forbidden=set('the a and in of see cf so he this for as it on to at i is an that with non et cum si ad'.split())
cues=r'(?:[“‘\x27\"]|(?:[Tt]he|[Tt]his|[Aa]s|[Aa]n?|[Ss]ee|[Cc]p\.|[Cc]f\.|[Ss]o|[Ff]or|[Ii]n|[Oo]n|[Ww]ith|[Bb]y|[Ff]rom|[Ii]t|[Hh]e|[Hh]is|[Tt]o|[Bb]ut|[Oo]f|[Ww]hen|[Ww]hile|[Ii]s|[Ww]as|[Aa]re|[Tt]hat|[Uu]sed|[Mm]eans|[Rr]efers|[Ii]\.e\.|[Ii]nstead)\b)'
notes=[]
for hi,h in enumerate(heads):
 ch=h['ch'];lo=h['offset'];up=heads[hi+1]['offset'] if hi+1<len(heads) else len(s);part=s[lo:up];ws=tokens(part);lookup={}
 for sec in refs[str(ch)]:
  ts=[x[0] for x in tokens(sec['text'])]
  for j,w in enumerate(ts):lookup.setdefault(w,[]).append((sec['sec'],ts,j))
 cuts=[]
 for i,(w,a,b) in enumerate(ws):
  if w not in lookup:continue
  prefix=part[max(0,a-7):a];line=a==0 or ('\n' in prefix and not prefix.rsplit('\n',1)[1].strip());head=a<=len(str(ch))+3;punct=bool(re.search(r'[.—:]\s*$',prefix))
  if not(line or head or punct):continue
  poss=[]
  for sec,ts,j in lookup[w]:
   end=b;z=1;jj=j
   while z<=15:
    tail=part[end:end+90];length=z
    if (z>1 or w not in forbidden or head) and (re.match(r'[.,:;]?\s*'+cues,tail) or re.match(r'[.:]\s+[A-Z]',tail) and (line or head or z>1)):
     poss.append((length,sec,end))
    if i+z>=len(ws) or jj+1>=len(ts):break
    between=part[end:ws[i+z][1]];nw=ws[i+z][0]
    if re.search(r'[^.\s…–—-]',between) or len(between)>12:break
    if ts[jj+1]==nw:jj+=1
    elif '...' in between or '…' in between:
     hits=[k for k in range(jj+1,len(ts)) if ts[k]==nw]
     if not hits:break
     jj=hits[0]
    else:break
    end=ws[i+z][2];z+=1
   
  if poss:
   mx=max(x[0] for x in poss);best=[x for x in poss if x[0]==mx];end=best[0][2];cuts.append(dict(start=a,end=end,lemma=part[a:end],candidates=sorted(set(x[1] for x in best))))
 selected=[]
 for c in cuts:
  if not selected or c['start']>=selected[-1]['end']:selected.append(c)
 # Source chapter numeral is retained with the first note.
 if selected and part[:selected[0]['start']].strip().rstrip('.')==str(ch):selected[0]['prefix']=0
 elif not selected or selected[0]['start']>0:selected.insert(0,dict(start=0,end=0,lemma=None,candidates=[]))
 for i,c in enumerate(selected):
  a=c.get('prefix',c['start']);end=selected[i+1].get('prefix',selected[i+1]['start']) if i+1<len(selected) else len(part);txt=part[a:end]
  if not txt.strip():continue
  locs=c['candidates'];target=locs[0] if len(locs)==1 else None;evidence='Unique lemma phrase in Ihm section (provisional automatic match)' if target else 'Unresolved; no exact section attachment asserted'
  if target is None and locs:
   prev=notes[-1]['section'] if notes and notes[-1]['chapter']==ch else None;nxt=next((x['candidates'][0] for x in selected[i+1:] if len(x['candidates'])==1),None)
   if prev==nxt and prev in locs:target=prev;evidence='Repeated lemma between notes uniquely matching the same section'
  notes.append(dict(id=f'shuck.note.{len(notes)+1}',chapter=ch,section=target,lemma=c['lemma'],lemma_start=c['start']-a,lemma_length=c['end']-c['start'],text=txt,offset=lo+a,candidates=locs,evidence=evidence))
assert re.sub(r'\s+','',''.join(n['text'] for n in notes))==re.sub(r'\s+','',s)
(R/'notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2));(O/'chapter-heading-inventory.json').write_text(json.dumps(heads,ensure_ascii=False,indent=2))
print('Notes',len(notes),'lemmas',sum(bool(n['lemma']) for n in notes),'unresolved',sum(n['section'] is None for n in notes));print('unresolved',[(n['id'],n['chapter'],n['lemma'],n['text'][:50]) for n in notes if n['section'] is None])
