from pathlib import Path
import json,re,unicodedata
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';ns=json.load(open(R/'reviewed-notes.json'));cs=json.load(open(R/'opening-candidates.json'));refs=json.load(open(R/'reference-sections.json'))['12']
selected=[2,3,5,6,7,8,11,12,16,18,19,22,24,26,28,29,30,32,35,38,40,42,43,44,45,46,47,49,50,51,52,53,54,55,56,60,61,63,64,65,67,68,69,71,73,74,76,77,79,80,81,82,83,84,88,89,90,93,95,96,97,98,99,100,103,104,105,107,108,109,110,111,112,113,114,115,116,117,118,120,121,122,123,124,125,126,127,128,130,131,132,133,135,136,137,140,143,144,145,146,149,150,151,152,153,154,155,156,157,158,159,162,163,165,166,167,168,170,172,173,175,176,177,178,179,180,181,182,185,187,188,189]
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower().replace('v','u').replace('j','i')) if c.isalpha())
out=[];dec=[]
for n in ns:
 cuts=[dict(c,index=i) for i,c in enumerate(cs) if i in selected and c['parent']==n['id']];cuts.sort(key=lambda c:c['offset']);old=n['text'];n['text']=old[:cuts[0]['offset']] if cuts else old;out.append(n)
 for j,c in enumerate(cuts):
  lemma=c['lemma'];ws=[norm(w) for w in re.findall(r'[^\W\d_]+',lemma)];hits=[]
  for r in refs[str(n['chapter'])]:
   ts=[norm(w) for w in re.findall(r'[^\W\d_]+',r['text'])];pos=0
   for w in ws:
    try:pos=ts.index(w,pos)+1
    except ValueError:break
   else:hits.append(r['sec'])
  sec=hits[0] if len(hits)==1 else None
  # For single words repeated within a chapter require both surrounding notes to agree.
  if sec is None and n['section'] in hits:
   nxt=next((x for x in ns if x['offset']>n['offset'] and x['chapter']==n['chapter']),None)
   if nxt and nxt['section']==n['section']:sec=n['section']
  end=cuts[j+1]['offset'] if j+1<len(cuts) else len(old);new=dict(id=f'shuck.extra.{c["index"]}',chapter=n['chapter'],section=sec,lemma=lemma,lemma_start=0,lemma_length=len(lemma),text=old[c['offset']:end],offset=n['offset']+c['offset'],candidates=hits,evidence='Reviewed source lemma opening; unique ordered Latin words in section' if sec else 'Reviewed lemma; section attachment unresolved')
  out.append(new);dec.append(dict(id=new['id'],lemma=lemma,chapter=n['chapter'],section=sec,candidates=hits))
(R/'final-notes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));(O/'additional-lemma-review.json').write_text(json.dumps(dec,ensure_ascii=False,indent=2));print('Final',len(out));print('Unresolved',[(n['id'],n['chapter'],n['lemma'],n['candidates']) for n in out if n['section'] is None])
