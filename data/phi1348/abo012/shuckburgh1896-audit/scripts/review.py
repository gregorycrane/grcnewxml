from pathlib import Path
import json,re
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';ns=json.load(open(R/'notes.json'));ledger=[]
remove=set([10,29,59,70,110,112,113,114,138,139,142,147,167,168,171,217,226,240,259,332,334,337,339,348,352,376,394,408,410,411,454,461,471,476,499,509,539,576,608,653,706,711,724,753,778,811,835,839,847,899,908,910,994])
# Name initials within quotations, inscriptions, and stemmata are not annotation lemmas.
for n in ns:
 if n['lemma'] and len(re.sub(r'\W','',n['lemma']))<=2:remove.add(int(n['id'].split('.')[-1]))
remove.discard(980)
# Preserve each source chapter's opening; identify its fuller lemma below.
reviewed=[]
for n in ns:
 i=int(n['id'].split('.')[-1])
 if i in remove and reviewed and reviewed[-1]['chapter']==n['chapter']:
  reviewed[-1]['text']+=n['text'];ledger.append(dict(id=n['id'],action='Merge false lemma split into preceding commentary',before=n['lemma']))
 else:reviewed.append(n)
# Pull back a lemma fragment when its source prefix was stranded in the preceding note.
pull={8:'reliquiae...',118:'iussus...',190:'17. reconciliationibus... ',328:'decurias...',412:'Kal. ',840:'praecipuam...'}
for i,prefix in pull.items():
 at=next(j for j,n in enumerate(reviewed) if n['id']==f'shuck.note.{i}');n=reviewed[at];prev=reviewed[at-1];assert prev['text'].endswith(prefix),(i,prev['text'][-60:]);prev['text']=prev['text'][:-len(prefix)];n['text']=prefix+n['text'];n['offset']-=len(prefix);n['lemma_start']=len('17. ') if i==190 else 0;n['lemma_length']+=len(prefix)-n['lemma_start'];n['lemma']=n['text'][n['lemma_start']:n['lemma_start']+n['lemma_length']]
reviewed=[n for n in reviewed if n['text'].strip()]
manual={35:('divisores operasque campestris','1'),67:('avito suburbano','1'),106:('necem ... vindicare','1'),262:('Lollianam... Varianam','1'),405:('Senatorum numerum','1'),418:('ne acta...publicarentur','1'),436:('si deessent...senatores','1'),451:('liberalitatem…….exhibuit','1'),490:('Puteolis','1'),563:('diplomatibus','1'),781:('Cornelius Nepos tradit','1'),785:('post cibum meridianum','1'),824:('eloquentiam...exercuit','1'),829:('in coetu familiarium','1'),850:('autographae','1'),876:('Philippensi','1'),887:('Athenis initiatus','1'),922:('ingrediente eo urbem','1'),955:('mimum','1'),960:('duobus Sext....cons','1'),980:('L. Planco, C. Silio cons','1'),57:('VIIII. Kal. Oct','1'),624:('Kal. Ian. strenam','1'),658:('Iuliam L. Paulo censoris f','1'),340:('a M. Agrippa...egregia','5'),517:('ludis','3')}
# cons is a fragment of the chapter 100 opening, not a separate lemma.
i=next(i for i,n in enumerate(reviewed) if n['id']=='shuck.note.961');reviewed[i-1]['text']+=reviewed[i]['text'];reviewed.pop(i)
for n in reviewed:
 i=int(n['id'].split('.')[-1])
 if i in manual:
  lemma,sec=manual[i];a=n['text'].index(lemma);n.update(lemma=lemma,lemma_start=a,lemma_length=len(lemma),section=sec,evidence='Reviewed printed lemma opening and corresponding Ihm passage');ledger.append(dict(id=n['id'],action='Reviewed lemma and section',lemma=lemma,section=sec))
# Cross-page broken words, keeping the actual source form in the change ledger.
for n in reviewed:
 old=n['text'];a=n['lemma_start'];b=a+n['lemma_length']
 def clean(s):
  def f(m):ledger.append(dict(id=n['id'],action='Join page-spanning broken word',before=m[0],after=m[1]+m[2]));return m[1]+m[2]
  return re.sub(r'([^\W\d_]+)-\s*\n([a-z]+)',f,s)
 prefix=clean(old[:a]);lemma=clean(old[a:b]);body=clean(old[b:]);n.update(text=prefix+lemma+body,lemma_start=len(prefix),lemma_length=len(lemma),lemma=lemma if n['lemma'] else None)
(R/'reviewed-notes.json').write_text(json.dumps(reviewed,ensure_ascii=False,indent=2));(O/'review-decisions.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2));print(len(reviewed),sum(bool(n['lemma']) for n in reviewed));print([(n['id'],n['chapter'],n['lemma']) for n in reviewed if n['section'] is None])
