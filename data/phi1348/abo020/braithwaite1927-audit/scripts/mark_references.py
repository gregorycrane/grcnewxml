from pathlib import Path
from lxml import etree as E
import re,json
R=Path(__file__).parent;O=R.parents[1]/'outputs/Braithwaite-Vespasian';T='{http://www.tei-c.org/ns/1.0}';X='{http://www.w3.org/XML/1998/namespace}';records=[];stats={}
names='Dio|Dio Cassius|Dio Chrysost. Or.|Tac. Hist.|Tac. Ann.|Tac. H.|Tac. A.|Tac. Agr.|Tac. Dial.|Cic. Agr.|Cic. Att.|Cic. Fam.|Cic. Off.|Cic. Fin.|Cic. Mur.|Cic. N.D.|Cic. Sest.|Cic. Phil.|Cic. de Or.|Cic. Verr.|Plin. N.H.|Plin. Pan.|Plin. Ep.|Plin.|Plut. Galb.|Plut. Oth.|Plut. Caes.|Plut. Pomp.|Plut. Num.|Suet. Gramm.|Suet. Aug.|Suet. Tib.|Suet. Iul.|Suet. Claud.|Suet. Calig.|Suet. Ner.|Suet. Galb.|Suet. Oth.|Suet. Vitell.|Suet. Vesp.|Suet. Tit.|Suet. Dom.|Aug.|Tib.|Iul.|Claud.|Calig.|Ner.|Galb.|Oth.|Vitell.|Vesp.|Tit.|Dom.|Gell.|Eutrop.|Oros.|Val. Max.|Aur. Vict. Caes.|Aur. Vict.|Auson. Caes.|Auson.|Colum.|Prop.|Liv.|Juv.|Mart.|Hor. C.|Hor. Ep.|Hor. Sat.|Verg. Aen.|Virg. Aen.|Quintil.|Quint. Smyrn.|Quint.|Amm. Marc.|Appian Bell. Civ.|App. B.C.|Dion. Hal.|Varr. R.R.|Varro L.L.|C.I.L.|Nep. Attic.|Nep.|Frontin.|Strab.|Macrob. S.|Ov. Am.|Ov. Tr.|Ov. Met.|Ov. Fast.|Plaut. Trin.|Plaut. Pers.|Plaut.|Petron. Satyr.|Sen. Ep.|Sen.|Stat. Silv.|Silv.|Apul. Mag.|Curt.|Vell.'.split('|')
names += ['A. and G.','Hk.','Hark.','Roby','Zumpt','Vell.','Cic.','Gellius','Horace, Carm.','Horace, Epist.','Quintilian','Tacitus','Cicero','Plutarch','Plin. H. N.','Pliny, H.N.','Macrob. Sat.','Cic. pro Mur.','Cic. pro Sull.','Cic. in Cat.','Cic. ad Q. Frat.','Cic. pro Sest.','Cic. pro Mil.','Cic. Leg. Man.','Caes. Bell. Civil.','Dio Cass.','Dio. Cass.','Caes. B. G.','Caes. Bell. Civil.','Caes. Bell. Civ.','Caes. Bell. Gall.','Cic. de Rep.','Cic. de Leg.','Cic. de Off.','Cic. de Nat. Deor.','Cic. Tusc. Disp.','Cic. ad Fam.','Cic. ad Att.','Cic. Philipp.','Tac. Annal.','Tacit. Hist.','Tacit. Ann.','Pliny, H. N.','Pliny H. N.','Hor. Epist.','Quint. Inst.','Livy','Velleius','Plutarch, Caes.','Sallust, Cat.','Sall. Jug.']
names += ['Cato R. R.','Tac. A.','Tac. Ann.','M. A.','C. I. L.','Dio','Livy','Plut. Ant.','Cic. ad fam.','Cic. ad Att.','Cic. pro Mil.','Cic. de Off.','Ovid Met.','Vergil G.','Hor. Od.','Hor. S.','Hor. Sat.','Hor. Ep.','Seneca Ep.','Vell. Pat.','Plut. Cic.','Macr. Sat.','Plin. N. H.','Pliny N. H.','Pliny Ep.','Varro L. L.','Dig.','Iuv.','App. B. civ.','App. B. Civ.','Cic. 2 Phil.','Cic. Phil.','Cic. Tusc.','Ovid F.','Roby L. G.','Roby L. Gr.','Tacitus Agr.','Tacitus Ann.','Cicero de Off.','Tac. Germ.','Sen. de Clem.','Suet. Iul.','Suet. Cl.','Wilmanns']
names += ['Dessau','CIL.','CIL','ILS.','CIA.','Hist.','Ann.','B. I.','Martial','Dio','Gai. Inst.','Suet. Vit.','Suet. Ner.','Suet. Tit.','Suet. Dom.','Tac. Hist.','Tac. Ann.','Philostr. Apoll.','Epit.','Plut. Oth.']
num=r'(?:[ivxlcdm]+[.,]?\s*)?\d+[a-c]?(?:\s*[,\.]+\s*\d+[a-c]?)*(?:\s*[-–]\s*\d+)?'
pat=re.compile(r'(?<!\w)(?:'+ '|'.join(re.escape(x).replace(r'\ ',r'\s+') for x in sorted(names,key=len,reverse=True))+r')\s+'+num)
def wrap(parent,s,spans):
 parent.text=s[:spans[0][0]] if spans else s
 for i,(a,b,tag) in enumerate(spans):
  e=E.SubElement(parent,T+tag);e.text=s[a:b];e.tail=s[b:spans[i+1][0] if i+1<len(spans) else len(s)]
for path in O.glob('*com-eng1.xml'):
 tree=E.parse(str(path));before=''.join(tree.find('.//'+T+'body').itertext());nr=ng=nc=0
 for node in tree.findall('.//'+T+'note'):
  s=node.text or '';spans=[]
  # Explicit English definitions immediately following the lemma's colon.
  gm=re.match(r'[.,:]\s*[\x27"“‘]([^\x27"”’]+)[\x27"”’]',s)
  if gm:spans.append((gm.start(1),gm.end(1),'gloss'));ng+=1
  definitions={'braith.note.5':'a time-expired veteran re-engaged by a military commander','braith.note.7':'his profession was the collecting of debts at a commission','braith.note.10':'he was a moneylender','braith.note.139':'fitted a house out','braith.note.177':'the part of the day passed in solitude','braith.note.183':'appointed to the office','braith.note.188':'a comet'}
  if node.get(X+'id') in definitions:
   phrase=definitions[node.get(X+'id')];m=re.search(r'\s+'.join(re.escape(w) for w in phrase.split()),s);assert m;spans.append((m.start(),m.end(),'gloss'));ng+=1
  for m in pat.finditer(s):
   if any(a<=m.start()<b for a,b,t in spans):continue
   spans.append((m.start(),m.end(),'bibl'));nr+=1;records.append(dict(file=path.name,note=node.get(X+'id'),text=m.group()))
  spans.sort();wrap(node,s,spans)
 # Reviewed pairs from Galba 1: reference immediately followed by an exact quoted Latin extract.
 reviewed=[('Martial 5.84','Sane sic abeat meus December: scis certe, puto, vestra iam venire Saturnalia, Martias Kalendas; tunc reddam tibi, Galla, quod dedisti.'),('Tac. A. 12, 40','praecipuus scientia rei militaris.'),('Tac. Germ. 19','mulier, non forma non aetate maritum invenerit.'),('Caes. B. G. 1. 7','Caesar cum id nuntiatum esset eos (Helvetios) per provinciam nostram iter facere conari maturat ab urbe proficisci.'),('Tac. Ann. xiv 17','(Nero) qui unus\nsuperesset e familia summum ad fastigium genita'),('Cic. Agr. ii 25, 67','iugera trecenta, ubi institui vineae possunt.')]
 for b in list(tree.findall('.//'+T+'bibl')):
  for ref,q in reviewed:
   if re.sub(r'\s+',' ',''.join(b.itertext()))!=ref:continue
   tail=b.tail or '';m=re.match(r'[.,:]?\s*('+r'\s+'.join(re.escape(w) for w in q.split())+')',tail)
   if not m:continue
   par=b.getparent();idx=par.index(b);par.remove(b);cit=E.Element(T+'cit',type='textual');par.insert(idx,cit);cit.append(b);b.tail=tail[:m.start(1)];quote=E.SubElement(cit,T+'quote');quote.set(X+'lang','lat');quote.text=m.group(1);cit.tail=tail[m.end(1):];nc+=1
 assert ''.join(tree.find('.//'+T+'body').itertext())==before,path
 tree.write(str(path),encoding='UTF-8',xml_declaration=True,pretty_print=True);stats[path.name]=dict(bibl=nr,gloss=ng,cit=nc)
(O/'bibliographic-markup.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));(O/'markup-counts.json').write_text(json.dumps(stats,indent=2));print(stats)
