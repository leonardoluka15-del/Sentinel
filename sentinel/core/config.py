from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    database: str = str(Path(__file__).resolve().parents[2] / 'data' / 'sentinel.db')
    host: str = '127.0.0.1'
    port: int = 8501
    interval: float = 5.0
    token: str = ''
