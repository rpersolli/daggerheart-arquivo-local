import sys,json,uuid,io,re,argparse,threading,unicodedata
from pathlib import Path
from urllib.parse import urlparse,parse_qs,unquote
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import fitz
DATA=ROOT/'data';DATA.mkdir(exist_ok=True)
LOCK=threading.Lock()
INDEX=json.loads((DATA/'index.json').read_text(encoding='utf-8'))
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
for row in INDEX:row['search']=norm(row['text'])
def fields(path):
 doc=fitz.open(path); result=[]
 for p in doc:
  for w in p.widgets() or []:
   context=p.get_textbox(fitz.Rect(w.rect.x0-3,w.rect.y0-18,w.rect.x1+3,w.rect.y1+3)).strip().replace('\n',' / ')
   label=w.field_label or (context if context and len(context)<85 else w.field_name)
   if 'warrior' in path.name or (p.get_text().startswith('WARRIOR')):
    label={'Text Field0':'Nome','Text Field1':'Pronomes','Text Field2':'Herança','Text Field3':'Classe e subclasse','Text Field4':'Evasão','Text Field5':'Armadura','Text Field6':'Agilidade','Text Field7':'Força','Text Field8':'Acuidade','Text Field9':'Instinto','Text Field11':'Presença','Text Field12':'Conhecimento'}.get(w.field_name,label)
   result.append(dict(name=w.field_name,label=f'{len(result)+1}. {label}',value=w.field_value or '',type=w.field_type_string,page=p.number+1,choices=w.choice_values or [],on=w.on_state() if w.field_type_string in ['CheckBox','RadioButton'] else None))
 doc.close()
 return result
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/'public'),**kw)
 def log_message(self,*a):pass
 def send(self,value,status=200,mime='application/json; charset=utf-8'):
  b=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(b)));self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(b)
 def do_GET(self):
  u=urlparse(self.path);q=parse_qs(u.query)
  try:
   if u.path=='/api/search':
    term=norm(q.get('q',[''])[0]);words=term.split();out=[]
    if len(term)>=2:
     for row in INDEX:
      if all(w in row['search'] for w in words):
       i=row['search'].find(words[0]);out.append(dict(book=row['book'],page=row['page'],text=row['text'][max(0,i-90):i+330]))
       if len(out)>=60:break
    return self.send(out)
   if u.path=='/api/sheets':
    return self.send([json.loads(p.read_text(encoding='utf-8')) for p in DATA.glob('sheet-*.json')])
   if u.path=='/api/notes':return self.send(json.loads((DATA/'notes.json').read_text(encoding='utf-8')) if (DATA/'notes.json').exists() else [])
   if u.path=='/api/page':
    name=Path(q['file'][0]).name;p=int(q.get('page',['1'])[0])-1
    doc=fitz.open(ROOT/'public/books'/name)
    if p<0 or p>=len(doc):return self.send({'error':'Página inexistente'},400)
    image=doc[p].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).tobytes('png');doc.close()
    return self.send(image,mime='image/png')
   if u.path.startswith('/api/sheet/'):
    sid=u.path.rsplit('/',1)[1]
    if not re.fullmatch('[a-f0-9]{32}',sid):raise ValueError('Ficha inválida')
    pdf=DATA/f'{sid}.pdf'
    if 'page' in q:
     doc=fitz.open(pdf);p=doc[int(q['page'][0])-1]
     numbers={f['name']:i+1 for i,f in enumerate(fields(pdf))}
     for w in list(p.widgets() or []):
      num=numbers[w.field_name]
      p.insert_text((w.rect.x0,w.rect.y0+6),str(num),fontsize=6,color=(.65,0,0))
     image=p.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).tobytes('png');doc.close()
     return self.send(image,mime='image/png')
    if 'download' in q:return self.send(pdf.read_bytes(),mime='application/pdf')
    return self.send(fields(pdf))
   return super().do_GET()
  except Exception as e:self.send({'error':str(e)},400)
 def do_POST(self):
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length>40*1024*1024:return self.send({'error':'Limite de 40 MB por ficha'},413)
   # Requests from other origins must not mutate local files.
   origin=self.headers.get('Origin')
   if origin and urlparse(origin).netloc!=self.headers.get('Host'):return self.send({'error':'Origem inválida'},403)
   body=self.rfile.read(length);u=urlparse(self.path)
   if u.path=='/api/import':
    if not body.startswith(b'%PDF'):raise ValueError('Selecione um PDF válido')
    doc=fitz.open(stream=body,filetype='pdf')
    if doc.is_encrypted:raise ValueError('Remova a senha do PDF antes de importar')
    doc.close()
    sid=uuid.uuid4().hex;pdf=DATA/f'{sid}.pdf';pdf.write_bytes(body)
    fs=fields(pdf)
    if not fs:pdf.unlink();raise ValueError('Este PDF não tem campos editáveis. Use uma ficha fillable; o original permanece intacto.')
    name=parse_qs(u.query).get('name',['Personagem'])[0][:140]
    meta=dict(id=sid,name=name,fields=len(fs));(DATA/f'sheet-{sid}.json').write_text(json.dumps(meta,ensure_ascii=False),encoding='utf-8');return self.send(meta)
   if u.path=='/api/notes':
    notes=json.loads(body)
    if not isinstance(notes,list):raise ValueError('Notas inválidas')
    with LOCK:
     tmp=DATA/'notes.tmp';tmp.write_text(json.dumps(notes,ensure_ascii=False),encoding='utf-8');tmp.replace(DATA/'notes.json')
    return self.send({'ok':True})
   if u.path.startswith('/api/sheet/'):
    sid=u.path.rsplit('/',1)[1]
    if not re.fullmatch('[a-f0-9]{32}',sid):raise ValueError('Ficha inválida')
    values=json.loads(body);pdf=DATA/f'{sid}.pdf'
    with LOCK:
     doc=fitz.open(pdf)
     for p in doc:
      for w in p.widgets() or []:
       if w.field_name in values:
        w.field_value=values[w.field_name];w.update()
     b=doc.tobytes(garbage=3,deflate=True);doc.close()
     check=fitz.open(stream=b,filetype='pdf')
     for p in check:
      for w in p.widgets() or []:
       if w.field_name in values and str(w.field_value)!=str(values[w.field_name]):raise ValueError('Falha ao validar campo '+w.field_name)
     check.close()
     tmp=DATA/f'{sid}.tmp';tmp.write_bytes(b);tmp.replace(pdf)
    return self.send({'ok':True})
   self.send({'error':'Rota inexistente'},404)
  except Exception as e:self.send({'error':str(e)},400)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--lan',action='store_true');parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
 host='0.0.0.0' if args.lan else '127.0.0.1'
 print(f'Daggerheart local: http://127.0.0.1:{args.port}',flush=True)
 if args.lan:print('Modo rede local: todos na rede permitida pelo firewall podem acessar. Sem autenticação.',flush=True)
 ThreadingHTTPServer((host,args.port),Handler).serve_forever()
