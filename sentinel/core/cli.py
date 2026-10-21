import argparse
import logging
import os
from .config import Config
from .engine import Engine
from .worker import Worker
from sentinel.web.server import server

def main():
    parser=argparse.ArgumentParser(description='Sentinel network operations simulator')
    parser.add_argument('--host',default='127.0.0.1'); parser.add_argument('--port',type=int,default=int(os.getenv('PORT','8501')))
    parser.add_argument('--database',default=Config().database); parser.add_argument('--interval',type=float,default=5)
    args=parser.parse_args()
    if args.interval<1: parser.error('Interval must be at least one second')
    token=os.getenv('SENTINEL_TOKEN','')
    if args.host not in ('127.0.0.1','localhost','::1') and len(token)<16:
        parser.error('Remote binding requires SENTINEL_TOKEN of at least 16 characters')
    config=Config(database=args.database,host=args.host,port=args.port,interval=args.interval,token=token)
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
    engine=Engine(config); worker=Worker(engine,config.interval); http=server(engine,config)
    worker.start(); print(f'Sentinel simulation: http://{args.host}:{http.server_port}',flush=True)
    try: http.serve_forever()
    except KeyboardInterrupt: pass
    finally: worker.stop(); http.server_close()
