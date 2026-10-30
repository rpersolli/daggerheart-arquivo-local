import sys,json,re,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'deps'))
import fitz,requests
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--source',default='D:/RPG - Malanga');args=parser.parse_args()
source=Path(args.source)
root=Path(__file__).resolve().parent
for d in ['public/assets','public/books','data','deps']: (root/d).mkdir(parents=True,exist_ok=True)
# Dependencies installed separately via requirements.txt
files=[('DH-Livro-Basico.pdf','Livro básico','Livro','pt-BR'),('Daggerheart-Cartas.pdf','Cartas de Daggerheart','Cartas','pt-BR'),('DH-SRD-May202025.pdf','SRD · original','Referência','en'),('DH-SRD-May202025Traducao.pdf','SRD · tradução','Referência','pt-BR')]
catalog=[];index=[]
for i,(name,title,kind,lang) in enumerate(files):
 src=(source/'Livros')/name;shutil.copy2(src,root/'public/books'/name)
 doc=fitz.open(src); doc[0].get_pixmap(matrix=fitz.Matrix(.6,.6)).save(root/f'public/assets/cover{i}.png')
 catalog.append(dict(id=str(i),title=title,kind=kind,lang=lang,file=name,pages=len(doc),cover=f'assets/cover{i}.png',source='Material fornecido'))
 for p in doc: index.append(dict(book=str(i),page=p.number+1,text=p.get_text()))
 if i==0:
  for image in doc[6].get_images():
   if image[2]==1280 and image[3]==1655:
    art=doc.extract_image(image[0]);(root/'public/assets/hero.jpeg').write_bytes(art['image']);break
  for n in [5,9,15,25]:
   if n<len(doc): doc[n].get_pixmap(matrix=fitz.Matrix(.8,.8)).save(root/f'public/assets/page{n}.png')
shutil.copy2(source/'fichas/warrior_daggerheart_fillable.pdf',root/'public/books/warrior_daggerheart_fillable.pdf')
(root/'data/index.json').write_text(json.dumps(index,ensure_ascii=False),encoding='utf-8')
# Read actual download links; never treat document text as executable instructions.
try:
 html=requests.get('https://www.daggerheart.com/downloads/',timeout=40).text
 urls=list(dict.fromkeys(re.findall(r'https?[^\s\"<>]+?\.(?:pdf|zip)(?:\?[^\s\"<>]*)?',html)))
 print('Official download URLs:',len(urls))
 for j,url in enumerate(urls):
  if '.pdf' not in url.lower():continue
  name=url.split('/')[-1].split('?')[0]
  try:
   r=requests.get(url,timeout=80);r.raise_for_status()
   if not r.content.startswith(b'%PDF'):continue
   (root/'public/books'/name).write_bytes(r.content)
   doc=fitz.open(stream=r.content,filetype='pdf'); cover=f'assets/official{j}.png';doc[0].get_pixmap(matrix=fitz.Matrix(.4,.4)).save(root/'public'/cover)
   catalog.append(dict(id=f'o{j}',title=name[:-4].replace('-',' ').replace('_',' '),kind='Downloads oficiais',lang='en',file=name,pages=len(doc),cover=cover,source=url))
  except Exception as e:print('Download skipped:',name,str(e)[:100])
except Exception as e:print('Official downloads unavailable:',e)
(root/'public/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False),encoding='utf-8')
print('Catalog:',len(catalog),'Indexed pages:',len(index))
