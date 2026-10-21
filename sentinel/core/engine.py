import threading
from .database import Database
from .repository import Repository
from .inventory import devices
from .links import links
from .simulator import Simulator
from .incidents import Incidents
from .detection import detect
from .audit import record,recent
from .topology import impact,criticality
from .correlation import correlate
from .forecasting import forecast
from .sla import summarize
from .validation import identifier,integer
from sentinel.analytics.registry import analyze

class Engine:
    def __init__(self,config):
        self.lock=threading.RLock(); self.config=config
        self.db=Database(config.database); self.repo=Repository(self.db)
        self.nodes=devices(); self.edges=links(self.nodes); self.simulator=Simulator(self.nodes)
        self.incidents=Incidents(self.db)
        if not self.repo.latest(): self.repo.append(self.simulator.bootstrap(interval=config.interval))
        self.step(); record(self.db,'startup','Simulation engine initialized')
    def step(self):
        with self.lock:
            rows=self.simulator.sample(); self.repo.append(rows)
            for row,node in zip(rows,self.nodes):
                findings=detect(row,self.repo.history(row['device'],40),node['capacity'])
                self.incidents.reconcile(row['device'],findings)
    def scenario(self,scenario,target):
        with self.lock:
            self.simulator.set(scenario,target); record(self.db,'scenario',f'{scenario}: {target}'); self.step()
    def acknowledge(self,value):
        with self.lock:
            value=integer(value); self.incidents.acknowledge(value); record(self.db,'acknowledge',value)
    def snapshot(self,device=None):
        with self.lock:
            device=identifier(device or self.nodes[0]['id'],{n['id'] for n in self.nodes})
            history=self.repo.history(device,120); latest=self.repo.latest(); incidents=self.incidents.list()
            node=next(n for n in self.nodes if n['id']==device)
            return dict(mode='SIMULATION',nodes=self.nodes,links=self.edges,latest=latest,history=history,
                selected=device,incidents=incidents,correlations=correlate(incidents,self.nodes),
                analysis=analyze([r['cpu'] for r in history]),forecast=forecast(history,node['capacity']),
                sla=summarize([r for n in self.nodes for r in self.repo.history(n['id'],120)]),
                impact=impact(self.nodes,self.edges,device),criticality=criticality(self.nodes,self.edges)[:8],
                audit=recent(self.db),scenario=self.simulator.scenario,scenario_target=self.simulator.target,
                interval=self.config.interval)
