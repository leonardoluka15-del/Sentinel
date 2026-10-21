from .clock import now

class Incidents:
    def __init__(self,database): self.database=database
    def reconcile(self,device,findings):
        timestamp=now(); active={f['kind'] for f in findings}
        with self.database.connect() as db:
            for f in findings:
                prior=db.execute("SELECT id FROM incidents WHERE device=? AND kind=? AND status!='resolved'",(device,f['kind'])).fetchone()
                if prior:
                    db.execute('UPDATE incidents SET updated=?,detail=?,severity=? WHERE id=?',(timestamp,f['detail'],f['severity'],prior['id']))
                else:
                    db.execute("INSERT INTO incidents(opened,updated,device,kind,severity,status,detail) VALUES(?,?,?,?,?,'open',?)",(timestamp,timestamp,device,f['kind'],f['severity'],f['detail']))
            for row in db.execute("SELECT id,kind FROM incidents WHERE device=? AND status!='resolved'",(device,)).fetchall():
                if row['kind'] not in active: db.execute("UPDATE incidents SET status='resolved',updated=? WHERE id=?",(timestamp,row['id']))
            db.execute("DELETE FROM incidents WHERE status='resolved' AND id < (SELECT MAX(id)-5000 FROM incidents)")
    def acknowledge(self,incident_id):
        with self.database.connect() as db:
            cursor=db.execute("UPDATE incidents SET status='acknowledged',updated=? WHERE id=? AND status='open'",(now(),incident_id))
            if cursor.rowcount!=1: raise ValueError('Incident is not open')
    def list(self):
        with self.database.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM incidents ORDER BY id DESC LIMIT 250')]
