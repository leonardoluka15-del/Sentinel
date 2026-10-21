import math
import random
from datetime import datetime,timezone,timedelta
from .scenarios import SCENARIOS

class Simulator:
    def __init__(self,devices,seed=42):
        self.devices=devices; self.random=random.Random(seed); self.tick=0
        self.scenario='normal'; self.target=devices[0]['id']
    def set(self,scenario,target):
        if scenario not in SCENARIOS: raise ValueError('Unknown scenario')
        if target not in {d['id'] for d in self.devices}: raise ValueError('Unknown device')
        self.scenario=scenario; self.target=target
    def sample(self,ts=None):
        self.tick+=1; rows=[]; r=self.random
        target_index=next(i for i,d in enumerate(self.devices) if d['id']==self.target)
        for i,d in enumerate(self.devices):
            load=45+15*math.sin(self.tick/14+i/5)+r.gauss(0,3)
            cpu=load+r.gauss(0,2); latency=18+load/5+r.gauss(0,2)
            loss=max(0,r.gauss(0.12,0.08)); traffic=load/100*d['capacity']; available=1
            affected=d['id']==self.target
            downstream=self.scenario=='outage' and target_index%8==0 and i//8==target_index//8
            if affected:
                if self.scenario=='congestion': traffic=d['capacity']*0.97; latency+=100; cpu+=25
                elif self.scenario=='packet_loss': loss+=8; latency+=35
                elif self.scenario=='cpu_spike': cpu=97+r.random()*2
            if self.scenario=='outage' and (affected or downstream): available=0; traffic=0; loss=100; latency=0
            rows.append(dict(ts=ts or datetime.now(timezone.utc).isoformat(timespec='seconds'),device=d['id'],
                             cpu=round(min(100,max(0,cpu)),2),latency=round(max(0,latency),2),
                             loss=round(min(100,loss),2),traffic=round(traffic,2),available=available))
        return rows
    def bootstrap(self,count=72,interval=5):
        start=datetime.now(timezone.utc)-timedelta(seconds=count*interval)
        return [row for n in range(count) for row in self.sample((start+timedelta(seconds=n*interval)).isoformat(timespec='seconds'))]
