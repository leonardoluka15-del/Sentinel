from .clock import now

def record(database,action,detail):
    with database.connect() as db:
        db.execute('INSERT INTO audit(ts,action,detail) VALUES(?,?,?)',(now(),action,str(detail)))
        db.execute('DELETE FROM audit WHERE id < (SELECT MAX(id)-5000 FROM audit)')

def recent(database):
    with database.connect() as db:
        return [dict(r) for r in db.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 100')]
