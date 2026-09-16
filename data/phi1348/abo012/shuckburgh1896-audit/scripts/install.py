from pathlib import Path
from lxml import etree as E
import json,shutil,sys
R=Path(__file__).parent;O=R.parents[1]/'outputs/Shuckburgh-Augustus';D=Path('/Users/gcrane/github/grcnewxml/data/phi1348/abo012');rp=Path('/Users/gcrane/github/src-persverscomp/work_registry.json');w='phi1348.abo012';v='shuckburgh1896-com-eng1';name=w+'.'+v+'.xml';label='Commentary (Shuckburgh, 1896; English; OCR draft)';reg=json.loads(rp.read_text());reg[w].setdefault('commentaries',{})[v]={'path':str(D/name),'label':label,'class':'english-text'};reg[w]['strict_section_alignment']=True;t=E.parse(str(D/'__cts__.xml'));root=t.getroot();N='{http://chs.harvard.edu/xmlns/cts}';X='{http://www.w3.org/XML/1998/namespace}';urn='urn:cts:latinLit:'+w+'.'+v
for old in root.xpath('*[@urn="'+urn+'"]'):root.remove(old)
node=E.SubElement(root,N+'translation',urn=urn,workUrn='urn:cts:latinLit:'+w);node.set(X+'lang','eng')
for tag,s in [('label',label),('description','Evelyn S. Shuckburgh, C. Suetoni Tranquilli Divus Augustus. Cambridge University Press, 1896. Commentary collated from MDP and UC1 OCR witnesses, with Ihm chapter/section targets and mentioned/note lemma markup. OCR draft; see shuckburgh1896-audit for provenance, decisions and unresolved issues.')]:e=E.SubElement(node,N+tag);e.set(X+'lang','eng');e.text=s
stage=R/'install-stage';stage.mkdir(exist_ok=True);t.write(str(stage/'__cts__.xml'),encoding='UTF-8',xml_declaration=True,pretty_print=True);(stage/'work_registry.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
if '--apply' in sys.argv:
 shutil.copy2(O/name,D/name);shutil.copy2(stage/'__cts__.xml',D/'__cts__.xml');shutil.copy2(stage/'work_registry.json',rp);shutil.copytree(O,D/'shuckburgh1896-audit',dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.xml'));print('Installed commentary, CTS entry, registry and audit.')
else:print('Staged CTS and registry changes; no external files modified.')
