from pathlib import Path
import json,re
R=Path(__file__).parent;ns=json.load(open(R/'notes.json'));ledger=[];out=[]
for n in ns:
 i=int(n['id'].split('.')[-1])
 if i in [79,92,104,159,197]:out[-1]['text']+=n['text'];ledger.append(dict(id=n['id'],action='Merge false or fragmentary lemma split',lemma=n['lemma']))
 else:out.append(n)
manual={72:'manum humanam',80:'nec tamen fortuito favore',91:'Suscepto civili bello',95:'e plebe quidam ..nec eventus defuit',100:'Milites inter se agebant',103:'ac ne quam occasionem\n•\nrevocavit',138:'Vitelli hostis sui filiam',154:'negata sibi gratuita libertate',187:'Mausoleum',198:'adsiduas in se coniurationes',169:'per Kal. Mart',196:'extinctus est VIIII. Kal. Iul. septimum'}
for n in out:
 i=int(n['id'].split('.')[-1])
 if i in manual:
  lemma=manual[i];a=n['text'].index(lemma);n.update(lemma=lemma,lemma_start=a,lemma_length=len(lemma));ledger.append(dict(id=n['id'],action='Identify full printed lemma',lemma=lemma))
 # No lexical changes; join only remaining page-spanning word breaks.
 a=n['lemma_start'];b=a+n['lemma_length']
 def clean(s):
  def f(m):ledger.append(dict(id=n['id'],action='Join page-spanning hyphen',before=m[0],after=m[1]+m[2]));return m[1]+m[2]
  return re.sub(r'([^\W\d_]+)-\n([a-z]+)',f,s)
 pre,lem,tail=clean(n['text'][:a]),clean(n['text'][a:b]),clean(n['text'][b:]);n.update(text=pre+lem+tail,lemma_start=len(pre),lemma_length=len(lem),lemma=lem if n['lemma'] else None)
(R/'reviewed-notes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));(R.parents[1]/'outputs/Braithwaite-Vespasian/review-decisions.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
