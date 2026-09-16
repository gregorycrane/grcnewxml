from pathlib import Path
import json
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';ns=json.load(open(R/'corrected-notes.json'));ledger=[]
# Correct the truncated preposition using the second witness on page 33.
n=next(n for n in ns if n['id']=='shuck.note.175');old='er Mylas et Naulochum';new='inter Mylas et Naulochum';assert old in n['text'];n['text']=n['text'].replace(old,new);ledger.append(dict(id=n['id'],before=old,after=new,evidence='UC1 page 33'))
manual=[(16,'inter Mylas et Naulochum','1'),(31,'Diale flaminium','4'),(7,'gestu gustuve','2'),(10,'in locum Tribuni Plebeii','2'),(18,'ludos quinquennales','2'),(94,'exuviis Iovis 0. M','6'),(101,'cum duobus paternis hereditatibus','3'),(29,'amphitheatrum...Tauri','5'),(78,'residua diurni actus','1'),(71,'accesserunt','2'),(71,'geronticos','2'),(87,'versus, of a','3'),(87,'circumducit','3')]
for i,(ch,lemma,sec) in enumerate(manual):
 hits=[(j,n['text'].index(lemma)) for j,n in enumerate(ns) if n['chapter']==ch and lemma in n['text']];assert len(hits)==1,(lemma,hits);j,a=hits[0];n=ns[j];assert a>n['lemma_start']+n['lemma_length'];tail=n['text'][a:];n['text']=n['text'][:a];new=dict(id='shuck.manual.'+str(i),chapter=ch,section=sec,lemma=lemma,lemma_start=0,lemma_length=len(lemma),text=tail,offset=n['offset']+a,candidates=[sec],evidence='Reviewed source lemma and Ihm section');ns.insert(j+1,new);ledger.append(dict(id=new['id'],lemma=lemma,section=f'{ch}.{sec}',action='Recover embedded source note opening'))
 if lemma=='versus, of a':new.update(lemma='versus',lemma_length=6)
(R/'edition-notes.json').write_text(json.dumps(ns,ensure_ascii=False,indent=2));(O/'final-review-decisions.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2));print('Notes',len(ns))
