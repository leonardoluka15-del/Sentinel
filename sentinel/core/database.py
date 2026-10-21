import sqlite3
from contextlib import contextmanager
from pathlib import Path

class Database:
    def __init__(self,path):
        self.path=str(path)
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as db:
            db.executescript("""
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS samples(seq INTEGER PRIMARY KEY, ts TEXT, device TEXT, cpu REAL, latency REAL, loss REAL, traffic REAL, available INTEGER);
            CREATE INDEX IF NOT EXISTS sample_device ON samples(device,seq);
            CREATE TABLE IF NOT EXISTS incidents(id INTEGER PRIMARY KEY, opened TEXT, updated TEXT, device TEXT, kind TEXT, severity TEXT, status TEXT, detail TEXT);
            CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, ts TEXT, action TEXT, detail TEXT);
            """)
    @contextmanager
    def connect(self):
        db=sqlite3.connect(self.path,timeout=15)
        db.row_factory=sqlite3.Row
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback(); raise
        finally:
            db.close()
