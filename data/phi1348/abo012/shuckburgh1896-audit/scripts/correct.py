from pathlib import Path
import json,re
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';ns=json.load(open(R/'final-notes.json'));changes=json.load(open(O/'witness-differences.json'));pages=json.load(open(R/'page-offsets.json'));ledger=[]
selected=[1,26,45,155,192,203,207,213,267,309,311,403,406,515,516,519,526,542,546,602,614,616,641,655,674,705,740,746,753,769,808,819,901,924,930,970,990,1021,1097,1112,1127]
for i in selected:
 c=changes[i];pattern=r'(?<!\w)'+r'\s+'.join(re.escape(x) for x in c['mdp'].split())+r'(?!\w)';hits=[]
 for n in ns:
  pg=next(p['page'] for p in reversed(pages) if p['offset']<=n['offset']);endpg=next(p['page'] for p in reversed(pages) if p['offset']<=n['offset']+len(n['text'])+60)
  if not pg<=c['page']<=endpg:continue
  for m in re.finditer(pattern,n['text']):hits.append((n,m))
 if len(hits)!=1:print('SKIP',i,c['mdp'],len(hits));continue
 n,m=hits[0];a=n['lemma_start'];b=a+n['lemma_length'];delta=len(c['uc1'])-len(m[0]);n['text']=n['text'][:m.start()]+c['uc1']+n['text'][m.end():]
 if m.end()<=a:n['lemma_start']+=delta
 elif a<=m.start() and m.end()<=b:n['lemma_length']+=delta
 elif m.start()<b:raise AssertionError(c)
 n['lemma']=n['text'][n['lemma_start']:n['lemma_start']+n['lemma_length']];ledger.append(dict(witness_difference=i,note=n['id'],page=c['page'],before=m[0],after=c['uc1'],evidence='UC1 witness corroborates clear OCR repair'))
# Explicit source lemma has an edition conjunction difference from Ihm, but identifies section 27.3.
for n in ns:
 if n['id']=='shuck.extra.49':n.update(section='3',evidence='Reviewed source curiosum et speculatorem against Ihm curiosum ac speculatorem at 27.3; conjunction retained')
 if n['id']=='shuck.extra.172':
  lemma='saepius...cum P. R. belligeraverunt';assert n['text'].startswith(lemma);n.update(lemma=lemma,lemma_length=len(lemma),section='2',evidence='Reviewed source abbreviated P. R. and lemma against Ihm 94.2')
(R/'corrected-notes.json').write_text(json.dumps(ns,ensure_ascii=False,indent=2));(O/'witness-corrections.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2));print('Witness repairs',len(ledger))
