import json
import math
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from sentinel.core.config import Config
from sentinel.core.engine import Engine
from sentinel.core.graph import adjacency,components,shortest
from sentinel.analytics.registry import analyze
from sentinel.core.exports import csv_bytes
from sentinel.web.server import server

class SentinelTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.config=Config(database=str(Path(self.temp.name)/'test.db'),port=0)
        self.engine=Engine(self.config)
    def tearDown(self): self.temp.cleanup()
    def test_inventory_and_plugins(self):
        s=self.engine.snapshot()
        self.assertEqual(len(s['nodes']),48)
        self.assertEqual(len(s['analysis']),30)
        self.assertEqual(len(s['history']),73)
        self.assertTrue(all(math.isfinite(x) for x in s['analysis'].values()))
        self.assertEqual(analyze([1,2,3,4])['mean'],2.5)
        self.assertEqual(analyze([1,2,3,4])['slope'],1)
        self.assertEqual(analyze([1,2,3,4])['forecast'],10)
        self.assertEqual(analyze([])['mean'],0)
        self.assertEqual(analyze([5]*10)['variance'],0)
    def test_outage_propagation_and_recovery(self):
        self.engine.scenario('outage','SNT-001')
        s=self.engine.snapshot()
        self.assertEqual(sum(not r['available'] for r in s['latest']),8)
        active=[i for i in s['incidents'] if i['status']!='resolved']
        self.assertEqual(sum(i['kind']=='availability' for i in active),8)
        self.engine.acknowledge(active[0]['id'])
        self.assertEqual(self.engine.incidents.list()[0]['status'],'acknowledged')
        self.engine.scenario('normal','SNT-001')
        self.assertTrue(all(i['status']=='resolved' for i in self.engine.incidents.list()))
    def test_leaf_outage(self):
        self.engine.scenario('outage','SNT-002')
        self.assertEqual(sum(not r['available'] for r in self.engine.repo.latest()),1)
    def test_congestion_cpu_loss(self):
        for scenario,kind in [('congestion','capacity'),('cpu_spike','cpu'),('packet_loss','packet_loss')]:
            self.engine.scenario(scenario,'SNT-002')
            self.assertIn(kind,[i['kind'] for i in self.engine.incidents.list() if i['status']=='open'])
    def test_validation_and_topology(self):
        for scenario,target in [('bogus','SNT-001'),('normal','bad')]:
            with self.assertRaises(ValueError): self.engine.scenario(scenario,target)
        with self.assertRaises(ValueError): self.engine.snapshot('bad')
        with self.assertRaises(ValueError): self.engine.acknowledge(True)
        s=self.engine.snapshot(); self.assertEqual(s['impact']['impacted_count'],8)
        graph=adjacency(s['nodes'],s['links'])
        self.assertEqual(len(components(graph)),1)
        self.assertEqual(shortest(graph,'SNT-002','SNT-003'),['SNT-002','SNT-001','SNT-003'])
    def test_persistence_export(self):
        self.engine.scenario('packet_loss','SNT-002')
        fresh=Engine(self.config)
        self.assertGreater(len(fresh.repo.history('SNT-002')),73)
        self.assertEqual(fresh.simulator.scenario,'normal')
        self.assertIn(b'traffic',csv_bytes(fresh.repo.history('SNT-002')))
    def test_http_security_and_actions(self):
        self.config.token='test-token-123456789'
        http=server(self.engine,self.config)
        thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
        base='http://127.0.0.1:'+str(http.server_port)
        def request(path,body=None,token=True,origin=None):
            headers={}
            if token: headers['Authorization']='Bearer '+self.config.token
            if origin: headers['Origin']=origin
            data=json.dumps(body).encode() if body is not None else None
            return urlopen(Request(base+path,data=data,headers=headers),timeout=10)
        try:
            self.assertEqual(request('/health',token=False).status,200)
            self.assertIn(b'SENTINEL',request('/',token=False).read())
            with self.assertRaises(HTTPError) as e: request('/api/state',token=False)
            self.assertEqual(e.exception.code,401)
            self.assertEqual(len(json.load(request('/api/state'))['nodes']),48)
            self.assertEqual(request('/api/scenario',{'scenario':'outage','target':'SNT-001'}).status,200)
            with self.assertRaises(HTTPError) as e: request('/api/step',{},origin='https://evil.invalid')
            self.assertEqual(e.exception.code,403)
            with self.assertRaises(HTTPError) as e: request('/api/scenario',{'scenario':[],'target':'SNT-001'})
            self.assertEqual(e.exception.code,400)
            with self.assertRaises(HTTPError) as e: request('/api/state?device=bogus')
            self.assertEqual(e.exception.code,400)
            self.assertIn('text/csv',request('/api/export.csv').headers['Content-Type'])
        finally: http.shutdown();http.server_close();thread.join()

if __name__=='__main__': unittest.main()
