from pathlib import Path
import json,re
R=Path(__file__).parent;O=R.parents[1]/'outputs/Braithwaite-Vespasian';ns=json.load(open(R/'reviewed-notes.json'));cs=json.load(open(R/'opening-candidates.json'));selected=[i for i in range(len(cs)) if i not in [4,10,16,18]];out=[];dec=[]
for n in ns:
 cuts=[dict(c,index=i) for i,c in enumerate(cs) if i in selected and c['parent']==n['id']];cuts.sort(key=lambda c:c['offset']);old=n['text'];n['text']=old[:cuts[0]['offset']] if cuts else old;out.append(n)
 for j,c in enumerate(cuts):
  end=cuts[j+1]['offset'] if j+1<len(cuts) else len(old);new=dict(n,id='braith.extra.'+str(c['index']),text=old[c['offset']:end],lemma=c['lemma'],lemma_start=0,lemma_length=len(c['lemma']),offset=n['offset']+c['offset']);out.append(new);dec.append(dict(id=new['id'],action='Reviewed additional lemma',lemma=new['lemma']))
# Further source openings whose punctuation, inflection or word order defeats literal matching.
manual=[(1,'Spoletium (Spoleto)','3'),(5,'acie Betriacensi','7'),(7,'Alexandriam obtineret','1'),(7,'ac statim nuntiantes','1'),(19,'Diodoro','1'),(12,'ne tribuniciam quidem potestatem','1'),(6,'V. Idus Iul','3')]
for i,(ch,lemma,sec) in enumerate(manual):
 hits=[]
 for j,n in enumerate(out):
  if n['chapter']!=ch:continue
  for m in re.finditer(r'(?m)^'+re.escape(lemma),n['text']):hits.append((j,m.start()))
 if len(hits)!=1:print('Needs review',ch,lemma,hits);continue
 j,a=hits[0];n=out[j]
 if a<=n['lemma_start']+n['lemma_length']:continue
 old=n['text'];n['text']=old[:a];new=dict(n,id='braith.manual.'+str(i),text=old[a:],lemma=lemma,lemma_start=0,lemma_length=len(lemma),offset=n['offset']+a,section=sec,evidence='Reviewed lemma opening within printed section');out.insert(j+1,new);dec.append(dict(id=new['id'],action='Reviewed additional lemma',lemma=lemma))
for ident,prefix in [('braith.note.101','Vitellianorum\n'),('braith.note.156','summa aerarii\n')]:
 j=next(j for j,n in enumerate(out) if n['id']==ident);n=out[j];prev=out[j-1];assert prev['text'].endswith(prefix);prev['text']=prev['text'][:-len(prefix)];n['text']=prefix+n['text'];n['offset']-=len(prefix);n['lemma_length']+=len(prefix);n['lemma']=n['text'][:n['lemma_length']];dec.append(dict(id=ident,action='Reunite split printed lemma',lemma=n['lemma']))
(R/'edition-notes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));(O/'additional-lemma-review.json').write_text(json.dumps(dec,ensure_ascii=False,indent=2));print('Notes',len(out),'lemmas',sum(bool(n['lemma']) for n in out))
