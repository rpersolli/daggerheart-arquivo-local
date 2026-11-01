from pathlib import Path
import json,re
import pymupdf as fitz

def generate(root):
 out=Path(root)/'docs';folder=out/'cards';folder.mkdir(exist_ok=True)
 classes=['Bardo','Druida','Guardião','Patrulheiro','Ladino','Serafim','Feiticeiro','Guerreiro','Mago']
 domains=['Arcano','Lâmina','Falange','Códice','Graça','Meia-noite','Sabedoria','Esplendor','Valor']
 class_domains={'Bardo':['Códice','Graça'],'Druida':['Arcano','Sabedoria'],'Guardião':['Lâmina','Valor'],'Patrulheiro':['Falange','Sabedoria'],'Ladino':['Meia-noite','Graça'],'Serafim':['Esplendor','Valor'],'Feiticeiro':['Arcano','Meia-noite'],'Guerreiro':['Lâmina','Falange'],'Mago':['Códice','Esplendor']}
 cards=[]
 with fitz.open(out/'books/Daggerheart-Cartas.pdf') as doc:
  for page in doc:
   text=page.get_text();match=re.search(r'DH Básico\s+(\d+)/270',text)
   if not match:continue
   number=int(match[1]);i=number-1;lines=[x.strip() for x in text.splitlines() if x.strip()]
   data=dict(id=f'dh-card-{number:03}',number=number,page=page.number+1,image=f'cards/{number:03}.png',text=text,classes=[],domain='',stage='',level='')
   if i<54:
    data.update(category='Subclasse',title=lines[2].title(),stage=lines[3].capitalize(),classes=[classes[i//6]])
   elif i<72:
    names=[x for x in lines if x!='ANCESTRALIDADE'];data.update(category='Ancestralidade',title=names[0].title())
   elif i<81:
    names=[x for x in lines if not x.replace(' ','').upper()=='COMUNIDADE'];data.update(category='Comunidade',title=names[0].title())
   else:
    domain=domains[(i-81)//21];level=next(w[4] for w in page.get_text('words') if w[0]<60 and w[1]<35 and w[4].isdigit());data.update(category='Domínio',title=lines[3],domain=domain,level=level,kind=lines[2].capitalize(),classes=[c for c,ds in class_domains.items() if domain in ds])
   page.get_pixmap(matrix=fitz.Matrix(2.5,2.5),alpha=False).save(out/data['image']);cards.append(data)
 assert len(cards)==270, f'Expected 270 fronts; found {len(cards)}'
 (out/'cards.json').write_text(json.dumps(cards,ensure_ascii=False),encoding='utf-8')
 print('Generated',len(cards),'card fronts; card backs excluded.')

if __name__=='__main__':generate(Path(__file__).resolve().parent)
