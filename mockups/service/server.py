#!/usr/bin/env python3
"""Loopback-only document workspace. Python standard library + macOS Vision/PDFKit."""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import re
import secrets
import sqlite3
import subprocess
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(os.environ.get('MDP_DATA_DIR', Path.home() / 'Library/Application Support/MedDataPlatform'))
DB = DATA / 'workspace.sqlite3'
MAX_FILE = 10 * 1024 * 1024
POOL = concurrent.futures.ThreadPoolExecutor(max_workers=2)
SLOTS = threading.BoundedSemaphore(4)
LOCAL_HOSTS = {'127.0.0.1', 'localhost', '[::1]'}
ANALYTES = [
 ('glucose', r'glucose|глюкоза|глюкозы', 'Glucose'),
 ('hemoglobin', r'hemoglobin|haemoglobin|гемоглобин|\bhgb\b|\bhb\b', 'Hemoglobin'),
 ('platelets', r'platelets|тромбоциты|тромбоцитов|\bplt\b', 'Platelets'),
 ('leukocytes', r'leukocytes|white blood cells|лейкоциты|\bwbc\b', 'White blood cells'),
 ('erythrocytes', r'erythrocytes|red blood cells|эритроциты|\brbc\b', 'Red blood cells'),
 ('creatinine', r'creatinine|креатинин', 'Creatinine'),
 ('cholesterol', r'cholesterol|холестерин', 'Cholesterol'),
 ('crp', r'c-reactive protein|с-реактивный белок|\bcrp\b|\bсрб\b', 'C-reactive protein'),
 ('alt', r'alanine aminotransferase|\balt\b|\bалт\b', 'ALT'),
 ('ast', r'aspartate aminotransferase|\bast\b|\bаст\b', 'AST'),
 ('tsh', r'thyroid stimulating hormone|\btsh\b|\bттг\b', 'TSH'),
 ('hba1c', r'hba1c|гликированный гемоглобин', 'HbA1c'),
]
NUMBER = r'[-+]?\d+(?:[.,]\d+)?'
UNIT = r'(?:10\s*\^?\s*[129]{1,2}\s*/\s*[lл]|[×x]\s*10\s*\^?\s*[129]{1,2}\s*/\s*[lл]|mmol\s*/\s*[lL]|mg\s*/\s*d[lL]|[µμu]mol\s*/\s*[lL]|g\s*/\s*[lL]|g\s*/\s*d[lL]|mg\s*/\s*[lL]|[µμu]IU\s*/\s*m[lL]|mIU\s*/\s*[lL]|[uU]\s*/\s*[lL]|ммоль\s*/\s*л|мкмоль\s*/\s*л|мг\s*/\s*л|г\s*/\s*л|ед\s*/\s*л|%)'

def connect():
    connection = sqlite3.connect(DB, timeout=20)
    connection.row_factory = sqlite3.Row
    return connection

def initialize():
    DATA.mkdir(parents=True, exist_ok=True, mode=0o700)
    (DATA / 'files').mkdir(exist_ok=True, mode=0o700)
    os.chmod(DATA, 0o700)
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS documents (
          id TEXT PRIMARY KEY, name TEXT NOT NULL, ext TEXT NOT NULL, size INTEGER NOT NULL,
          created TEXT NOT NULL, status TEXT NOT NULL, text TEXT DEFAULT '', pages TEXT DEFAULT '[]',
          results TEXT DEFAULT '[]', error TEXT DEFAULT '', measured TEXT DEFAULT '', published INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS notes (id TEXT PRIMARY KEY, kind TEXT NOT NULL, text TEXT NOT NULL, created TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS feedback (id TEXT PRIMARY KEY, document_id TEXT NOT NULL, text TEXT NOT NULL, created TEXT NOT NULL);
        ''')
        db.execute("UPDATE documents SET status='failed', error='Processing was interrupted. Retry the document.' WHERE status IN ('uploaded','processing')")
    os.chmod(DB, 0o600)

def parse_results(pages):
    """Only supported named rows; retain page and exact recognized row for review."""
    output = []
    measured = ''
    for page_no, text in enumerate(pages, 1):
        date_match = re.search(r'\b(20\d{2})[-/.](\d{2})[-/.](\d{2})\b', text)
        other = re.search(r'\b(\d{2})[./](\d{2})[./](20\d{2})\b', text)
        candidate = '-'.join(date_match.groups()) if date_match else '-'.join(reversed(other.groups())) if other else ''
        if candidate:
            try: measured = dt.date.fromisoformat(candidate).isoformat()
            except ValueError: pass
        for line in text.splitlines():
            # Match longest analyte name first, preserving source order around the result.
            matches = [(re.search(pattern, line, re.I), key, label) for key, pattern, label in ANALYTES]
            matches = sorted([m for m in matches if m[0]], key=lambda m: -len(m[0].group()))
            if not matches: continue
            match, key, label = matches[0]
            tail = line[match.end():].strip(' :|\t')
            value_match = re.match(r'(?P<value>' + NUMBER + r')\s*(?P<unit>' + UNIT + r')', tail, re.I)
            if not value_match: continue
            value = float(value_match['value'].replace(',', '.'))
            unit = re.sub(r'\s+', '', value_match['unit'])
            rest = tail[value_match.end():]
            interval = re.search(r'(?<!\d)(' + NUMBER + r')\s*[-–—]\s*(' + NUMBER + r')', rest)
            low = float(interval[1].replace(',', '.')) if interval else None
            high = float(interval[2].replace(',', '.')) if interval else None
            if low is not None and low > high: low = high = None
            output.append({'id': secrets.token_hex(5), 'analyte': key, 'name': label, 'value': value,
                           'unit': unit, 'low': low, 'high': high, 'page': page_no, 'source': line.strip()})
    return output, measured

def process_document(document_id):
    try:
        with connect() as db:
            row = db.execute('SELECT * FROM documents WHERE id=?', (document_id,)).fetchone()
            db.execute("UPDATE documents SET status='processing', error='' WHERE id=?", (document_id,))
        result = subprocess.run([str(DATA / 'recognize'), str(DATA / 'files' / (row['id'] + row['ext']))], capture_output=True, timeout=120)
        if result.returncode: raise ValueError(result.stderr.decode(errors='replace')[:350] or 'This document could not be read.')
        recognized = json.loads(result.stdout)
        if len(recognized.get('text', '').strip()) < 15: raise ValueError('No readable text was found. Try a sharper, well-lit photograph.')
        results, measured = parse_results(recognized['pages'])
        with connect() as db:
            db.execute("UPDATE documents SET status='ready', text=?, pages=?, results=?, measured=? WHERE id=?",
                       (recognized['text'], json.dumps(recognized['pages']), json.dumps(results), measured, document_id))
    except subprocess.TimeoutExpired:
        with connect() as db: db.execute("UPDATE documents SET status='failed', error=? WHERE id=?", ('Recognition exceeded two minutes. Try a shorter document.', document_id))
    except Exception as exc:
        with connect() as db: db.execute("UPDATE documents SET status='failed', error=? WHERE id=?", (str(exc)[:350], document_id))
    finally: SLOTS.release()

def document_dict(row, detail=False):
    item = dict(row)
    if detail:
        item['pages'] = json.loads(item['pages'])
        item['results'] = json.loads(item['results'])
    else:
        item['result_count'] = len(json.loads(item.pop('results')))
        item.pop('text'); item.pop('pages')
    return item

class Handler(BaseHTTPRequestHandler):
    server_version = 'MedDataLocal/1.0'
    def log_message(self, fmt, *args): pass
    def finish_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' blob: data:; media-src 'self' blob:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'")
        self.end_headers()
    def reply(self, code, value):
        raw = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json; charset=utf-8'); self.send_header('Content-Length', str(len(raw))); self.finish_headers(); self.wfile.write(raw)
    def allowed(self):
        host = self.headers.get('Host', '')
        if host not in {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}: return False
        origin = self.headers.get('Origin')
        return not origin or origin in {f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}
    def do_GET(self):
        if not self.allowed(): return self.reply(403, {'error':'Local access only.'})
        path = urlsplit(self.path).path
        if path == '/api/workspace':
            with connect() as db:
                docs = [document_dict(row) for row in db.execute('SELECT * FROM documents ORDER BY created DESC')]
                labs = []
                for row in db.execute('SELECT * FROM documents WHERE published=1 ORDER BY measured'):
                    for item in json.loads(row['results']): labs.append(item | {'document_id':row['id'], 'date':row['measured'], 'document_name':row['name']})
                notes = [dict(row) for row in db.execute('SELECT * FROM notes ORDER BY created DESC')]
            return self.reply(200, {'documents':docs,'labs':labs,'notes':notes})
        match = re.fullmatch(r'/api/documents/([a-f0-9]{32})(/file)?', path)
        if match:
            with connect() as db: row = db.execute('SELECT * FROM documents WHERE id=?', (match[1],)).fetchone()
            if not row: return self.reply(404, {'error':'Document not found.'})
            if not match[2]: return self.reply(200, document_dict(row, True))
            file = DATA / 'files' / (row['id'] + row['ext'])
            raw = file.read_bytes()
            self.send_response(200); self.send_header('Content-Type', mimetypes.guess_type(file.name)[0] or 'application/octet-stream'); self.send_header('Content-Disposition', 'inline; filename="document'+row['ext']+'"'); self.send_header('Content-Length',str(len(raw)));self.finish_headers();self.wfile.write(raw);return
        if path.startswith('/api/'): return self.reply(404, {'error':'Not found.'})
        relative = unquote(path).lstrip('/') or 'index.html'
        target = (ROOT / relative).resolve()
        if not target.is_relative_to(ROOT) or 'service' in target.relative_to(ROOT).parts or target.suffix not in {'.html','.css','.js','.png'}: return self.reply(404, {'error':'Not found.'})
        if not target.is_file(): return self.reply(404, {'error':'Not found.'})
        raw = target.read_bytes(); self.send_response(200); self.send_header('Content-Type', (mimetypes.guess_type(target.name)[0] or 'application/octet-stream') + ('; charset=utf-8' if target.suffix in {'.html','.js','.css'} else '')); self.send_header('Content-Length',str(len(raw)));self.finish_headers();self.wfile.write(raw)
    def do_POST(self):
        if not self.allowed(): return self.reply(403, {'error':'Local access only.'})
        path = urlsplit(self.path).path
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length <= 0 or length > MAX_FILE: return self.reply(413, {'error':'Choose a file smaller than 10 MiB.'})
            body = self.rfile.read(length)
            if path == '/api/documents':
                if not SLOTS.acquire(blocking=False): return self.reply(429, {'error':'Several documents are being processed. Please try again shortly.'})
                try:
                    ext = '.pdf' if body.startswith(b'%PDF-') else '.png' if body.startswith(b'\x89PNG\r\n\x1a\n') else '.jpg' if body.startswith(b'\xff\xd8\xff') else ''
                    if not ext: SLOTS.release(); return self.reply(415, {'error':'Choose a valid PDF, JPG or PNG file.'})
                    filename = unquote(self.headers.get('X-Filename', 'Document'))[:180].replace('\x00','')
                    document_id = secrets.token_hex(16)
                    destination = DATA / 'files' / (document_id + ext)
                    destination.write_bytes(body); os.chmod(destination, 0o600)
                    with connect() as db: db.execute('INSERT INTO documents(id,name,ext,size,created,status) VALUES(?,?,?,?,?,?)', (document_id,filename,ext,length,dt.datetime.now(dt.timezone.utc).isoformat(),'uploaded'))
                    POOL.submit(process_document, document_id)
                    return self.reply(202, {'id':document_id})
                except Exception: SLOTS.release(); raise
            payload = json.loads(body)
            if path == '/api/notes':
                text = str(payload.get('text','')).strip(); kind = payload.get('kind')
                if not text or len(text)>10000 or kind not in {'visit','prescription'}: return self.reply(400, {'error':'Enter a note of up to 10,000 characters.'})
                with connect() as db: db.execute('INSERT INTO notes VALUES(?,?,?,?)', (secrets.token_hex(16),kind,text,dt.datetime.now(dt.timezone.utc).isoformat()))
                return self.reply(201, {'saved':True})
            match = re.fullmatch(r'/api/documents/([a-f0-9]{32})/(retry|publish|feedback)', path)
            if not match: return self.reply(404, {'error':'Not found.'})
            document_id, action = match.groups()
            with connect() as db:
                row = db.execute('SELECT * FROM documents WHERE id=?',(document_id,)).fetchone()
                if not row: return self.reply(404, {'error':'Document not found.'})
                if action == 'feedback':
                    text = str(payload.get('text','')).strip()
                    if not text or len(text)>3000:return self.reply(400, {'error':'Describe the issue in up to 3,000 characters.'})
                    db.execute('INSERT INTO feedback VALUES(?,?,?,?)',(secrets.token_hex(16),document_id,text,dt.datetime.now(dt.timezone.utc).isoformat()))
                    return self.reply(201, {'saved':True})
                if action == 'retry':
                    if row['status']!='failed':return self.reply(409, {'error':'Only failed documents can be retried.'})
                    if not SLOTS.acquire(blocking=False):return self.reply(429, {'error':'Processing is busy. Try again shortly.'})
                    db.execute("UPDATE documents SET status='uploaded', error='' WHERE id=?",(document_id,))
                elif action == 'publish':
                    if row['published']: return self.reply(200, {'published':True,'already_published':True})
                    if row['status']!='ready':return self.reply(409, {'error':'Wait for processing to finish.'})
                    measured = dt.date.fromisoformat(str(payload.get('date',''))).isoformat()
                    edits = payload.get('results')
                    originals = json.loads(row['results'])
                    if not isinstance(edits,list) or not edits or {r.get('id') for r in edits}!={r['id'] for r in originals}:return self.reply(400, {'error':'Review every extracted result before confirmation.'})
                    original_by_id = {r['id']:r for r in originals}
                    results=[]
                    for edited in edits:
                        original=original_by_id[edited['id']]
                        value=float(edited['value']); low=float(edited['low']) if edited.get('low') not in (None,'') else None; high=float(edited['high']) if edited.get('high') not in (None,'') else None
                        import math
                        if not all(math.isfinite(v) for v in (value,low,high) if v is not None) or (low is not None and high is not None and low>high):raise ValueError('Check numeric values and reference limits.')
                        results.append(original|{'value':value,'low':low,'high':high,'reviewed':True})
                    db.execute('UPDATE documents SET published=1, measured=?, results=? WHERE id=?',(measured,json.dumps(results),document_id))
                    return self.reply(200, {'published':True})
            POOL.submit(process_document,document_id)
            return self.reply(202, {'id':document_id})
        except (ValueError,KeyError,TypeError) as exc: self.reply(400, {'error':str(exc)[:250] or 'Check the entered values.'})
        except Exception: self.reply(500, {'error':'The operation could not be completed. Your existing records have not been changed.'})

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
    initialize()
    binary=DATA/'recognize'; source=ROOT/'service/recognize.swift'
    if not binary.exists() or binary.stat().st_mtime<source.stat().st_mtime:
        print('Preparing local document recognition…',flush=True)
        subprocess.run(['/usr/bin/xcrun','swiftc',str(source),'-o',str(binary)],check=True)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'Medical Data Platform: http://127.0.0.1:{args.port}/index.html',flush=True)
    print('Document recognition runs on this Mac. Stop with Ctrl+C.',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close();POOL.shutdown(wait=False,cancel_futures=True)

if __name__=='__main__':main()
