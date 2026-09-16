from pathlib import Path
import json,re
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';ps=json.load(open(R/'commentary-pages.json'));s='';page_offsets=[];ledger=[]
for p in ps['mdp']:
 t=p['text'];page_offsets.append(dict(page=p['page'],offset=len(s),ch=p['ch']));s+=t+'\n'
# Rejoin page-spanning words when the other witness confirms the joined or identically broken spelling.
other='\n'.join(p['text'] for p in ps['uc1'])
def join(m):
 ledger.append(dict(kind='cross-page-hyphen',before=m[0],after=m[1]+m[2]));return m[1]+m[2]
# Keep page offsets stable by applying later only inside note text.
(R/'selected-com-12.txt').write_text(s);(R/'page-offsets.json').write_text(json.dumps(page_offsets,indent=2))
heads=[]
for m in re.finditer(r'(?m)^(\d{1,3})\.\s*',s):
 ch=int(m[1]);page=next(p for p in reversed(page_offsets) if p['offset']<=m.start())
 if abs(ch-page['ch'])<=2:heads.append(dict(ch=ch,offset=m.start(),end=m.end(),page=page['page'],preview=s[m.start():m.start()+100].replace('\n',' ')))
(R/'head-candidates.json').write_text(json.dumps(heads,ensure_ascii=False,indent=2))
for h in heads:print(h['ch'],h['page'],h['preview'])
