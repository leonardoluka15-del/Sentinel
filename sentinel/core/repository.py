class Repository:
    def __init__(self,database): self.database=database
    def append(self,samples):
        with self.database.connect() as db:
            db.executemany('INSERT INTO samples(ts,device,cpu,latency,loss,traffic,available) VALUES(:ts,:device,:cpu,:latency,:loss,:traffic,:available)',samples)
            db.execute('DELETE FROM samples WHERE seq < (SELECT MAX(seq)-92160 FROM samples)')
    def history(self,device,limit=120):
        with self.database.connect() as db:
            rows=db.execute('SELECT * FROM samples WHERE device=? ORDER BY seq DESC LIMIT ?',(device,limit)).fetchall()
            return [dict(r) for r in reversed(rows)]
    def latest(self):
        with self.database.connect() as db:
            return [dict(r) for r in db.execute('SELECT s.* FROM samples s JOIN (SELECT device,MAX(seq) seq FROM samples GROUP BY device) x ON s.seq=x.seq ORDER BY s.device')]
