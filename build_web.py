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
for i,url in enumerate(urls):
 name=url.split('/')[-1].split('?')[0];target=out/'books'/name
 download(url,target)
 with fitz.open(target) as doc:
  cover=f'assets/official{i}.jpg';doc[0].get_pixmap(matrix=fitz.Matrix(.6,.6)).save(out/cover)
  catalog.append(dict(id=f'official-{i}',title=name[:-4].replace('-',' ').replace('_',' '),kind='Material oficial',file=name,cover=cover,pages=len(doc),source=url))
(out/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False),encoding='utf-8')
(out/'.nojekyll').touch()
print('Static site ready:',len(catalog),'official PDFs')
