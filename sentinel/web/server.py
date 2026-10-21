import json
import logging
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit,parse_qs
from .responses import send
from .security import authorized,same_origin
from sentinel.core.exports import csv_bytes,report_bytes
from sentinel.core.scenarios import SCENARIOS

ASSETS=Path(__file__).parent/'assets'

def server(engine,config):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,format,*args): logging.info(format,*args)
        def do_GET(self):
            parsed=urlsplit(self.path); path=parsed.path
            assets={'/':('index.html','text/html; charset=utf-8'),'/style.css':('style.css','text/css'),'/app.js':('app.js','text/javascript')}
            if path in assets:
                name,mime=assets[path]; return send(self,(ASSETS/name).read_bytes(),content_type=mime)
            if path=='/health': return send(self,{'status':'ok','mode':'simulation'})
            if not authorized(self,config.token): return send(self,{'error':'Access token required'},401)
            try:
                device=parse_qs(parsed.query).get('device',[None])[0]
                if path=='/api/state': return send(self,engine.snapshot(device))
                if path=='/api/scenarios': return send(self,SCENARIOS)
                if path=='/api/export.csv': return send(self,csv_bytes(engine.snapshot(device)['history']),content_type='text/csv',filename='sentinel-telemetry.csv')
                if path=='/api/report.json': return send(self,report_bytes(engine.snapshot(device)),filename='sentinel-report.json')
                return send(self,{'error':'Not found'},404)
            except ValueError as exc: return send(self,{'error':str(exc)},400)
            except Exception: logging.exception('GET failed'); return send(self,{'error':'Internal error'},500)
        def do_POST(self):
            if not same_origin(self): return send(self,{'error':'Origin rejected'},403)
            if not authorized(self,config.token): return send(self,{'error':'Access token required'},401)
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=16384: return send(self,{'error':'Request size invalid'},413)
                payload=json.loads(self.rfile.read(size))
                if not isinstance(payload,dict): raise ValueError('Expected JSON object')
                if self.path=='/api/scenario': engine.scenario(payload.get('scenario'),payload.get('target'))
                elif self.path=='/api/acknowledge': engine.acknowledge(payload.get('id'))
                elif self.path=='/api/step': engine.step()
                else: return send(self,{'error':'Not found'},404)
                return send(self,{'ok':True})
            except (ValueError,TypeError) as exc: return send(self,{'error':str(exc)},400)
            except Exception: logging.exception('POST failed'); return send(self,{'error':'Internal error'},500)
    return ThreadingHTTPServer((config.host,config.port),Handler)
