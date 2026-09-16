from pathlib import Path
import json,re,difflib,hashlib
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus'
fix={4:21,6:11,14:22,24:14,28:15,29:15,30:13,36:13,50:15,53:18,60:19,62:24,66:11,69:16,72:18,76:18,82:15,83:9,84:11,87:18,88:16,100:18,110:11,112:21,114:17,118:24,120:20,126:19,132:20,134:21,136:17,138:19,139:16,141:17,144:14,146:26,148:26,150:22,153:22,154:12,156:36,161:23,174:22}
base=json.load(open(R/'mdp-pages.json'));other=json.load(open(R/'uc1-pages.json'));rows=json.load(open(R/'split-proposals.json'));ledger=[];outs={};splits=[]
for w,pages in [('mdp',base),('uc1',other)]:
 arr=[]
 for r in rows:
  n=r['page']
  if n>176:continue
  p=next(x for x in pages if x['label']==str(n));lines=p['text'].splitlines();sp=fix.get(n,r['split'])
  if w=='uc1':
   bp=next(x for x in base if x['label']==str(n));needle=' '.join('\n'.join(bp['text'].splitlines()[sp:]).split()[:22]).lower();best=None
   for i in range(3,min(len(lines),65)):
    cand=' '.join('\n'.join(lines[i:]).split()[:22]).lower();score=difflib.SequenceMatcher(None,needle,cand,autojunk=False).ratio()
    if best is None or score>best[0]:best=score,i
   sp=best[1];splits.append(dict(page=n,uc1_split=sp,similarity=round(best[0],3),first=lines[sp:sp+2]))
  s='\n'.join(lines[sp:]);before=s
  s=re.sub(r'\n(?:[0-9]+(?:[-–][0-9]+)?|[IVX]+[-–][0-9]+|S\.)\s*$','',s)
  if s!=before:ledger.append(dict(witness=w,page=n,kind='footer',removed=before[len(s):]))
  def join(m):
   ledger.append(dict(witness=w,page=n,kind='line-end-hyphen',before=m[0],after=m[1]+m[2]));return m[1]+m[2]
  s=re.sub(r'([^\W\d_]+)-\n([a-z]+)',join,s)
  arr.append(dict(page=n,scan=p['scan'],ch=r['ch'],text=s))
 outs[w]=arr
(R/'commentary-pages.json').write_text(json.dumps(outs,ensure_ascii=False,indent=2));(O/'cleanup-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2));(O/'page-stream-inventory.json').write_text(json.dumps([dict(page=r['page'],mdp_split=fix.get(r['page'],r['split']),**{k:v for k,v in s.items() if k!='page'}) for r,s in zip(rows,splits)],ensure_ascii=False,indent=2))
changes=[]
for a,b in zip(outs['mdp'],outs['uc1']):
 aa=a['text'].split();bb=b['text'].split()
 for op,i,j,k,l in difflib.SequenceMatcher(None,aa,bb,autojunk=False).get_opcodes():
  if op!='equal':changes.append(dict(page=a['page'],kind=op,mdp=' '.join(aa[i:j]),uc1=' '.join(bb[k:l]),context=' '.join(aa[max(0,i-5):min(len(aa),j+5)])))
(O/'witness-differences.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2));print('Differences',len(changes));print('Weak splits',[s for s in splits if s['similarity']<.8])
for w in ['mdp','uc1']:(O/(w+'-pages.json')).write_bytes((R/(w+'-pages.json')).read_bytes())
