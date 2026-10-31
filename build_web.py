"""Prepare the static site, including the free official download library."""
from pathlib import Path
import json,re,urllib.request,shutil
import pymupdf as fitz
import requests
ROOT=Path(__file__).resolve().parent;out=ROOT/'docs'
for folder in ['books','assets','vendor']:(out/folder).mkdir(parents=True,exist_ok=True)
def download(url,target):
 r=requests.get(url,timeout=120);r.raise_for_status();target.write_bytes(r.content)
vendor={'pdf.mjs':'https://cdn.jsdelivr.net/npm/pdfjs-dist@4.10.38/build/pdf.mjs','pdf.worker.mjs':'https://cdn.jsdelivr.net/npm/pdfjs-dist@4.10.38/build/pdf.worker.mjs','pdf-lib.min.js':'https://cdn.jsdelivr.net/npm/pdf-lib@1.17.1/dist/pdf-lib.min.js'}
for name,url in vendor.items():download(url,out/'vendor'/name)
urls=json.loads((ROOT/'official-downloads.json').read_text(encoding='utf-8'))
catalog=[]
index={}
for i,url in enumerate(urls):
 name=url.split('/')[-1].split('?')[0];target=out/'books'/name
 download(url,target)
 with fitz.open(target) as doc:
  cover=f'assets/official{i}.jpg';doc[0].get_pixmap(matrix=fitz.Matrix(.6,.6)).save(out/cover)
  catalog.append(dict(id=f'official-{i}',title=name[:-4].replace('-',' ').replace('_',' '),kind='Material oficial',file=name,cover=cover,pages=len(doc),source=url))
  index[f'official-{i}']=[dict(page=p.number+1,text=p.get_text()) for p in doc]
for i,(name,title) in enumerate([('DH-Livro-Basico.pdf','Livro básico'),('Daggerheart-Cartas.pdf','Cartas de Daggerheart'),('DH-SRD-May202025.pdf','SRD original'),('DH-SRD-May202025Traducao.pdf','SRD em português')]):
 target=out/'books'/name
 if not target.exists():download('https://github.com/rpersolli/daggerheart-arquivo-local/releases/download/v1.0.1/'+name,target)
 with fitz.open(target) as doc:
  cover=f'assets/book{i}.jpg';doc[0].get_pixmap(matrix=fitz.Matrix(.6,.6)).save(out/cover)
  catalog.insert(i,dict(id=f'book-{i}',title=title,kind='Livro',file=name,cover=cover,pages=len(doc)))
  index[f'book-{i}']=[dict(page=p.number+1,text=p.get_text()) for p in doc]
  if i==0:
   art=doc.extract_image(doc[6].get_images()[0][0]);(out/'assets/hero.jpeg').write_bytes(art['image'])
(out/'search-index.json').write_text(json.dumps(index,ensure_ascii=False),encoding='utf-8')
(out/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False),encoding='utf-8')
(out/'.nojekyll').touch()
print('Static site ready:',len(catalog),'official PDFs')
