import threading
import logging

class Worker:
    def __init__(self,engine,interval):
        self.engine=engine; self.interval=interval; self.stop_event=threading.Event()
        self.thread=threading.Thread(target=self.run,name='sentinel-simulator',daemon=True)
    def start(self): self.thread.start()
    def run(self):
        while not self.stop_event.wait(self.interval):
            try: self.engine.step()
            except Exception: logging.exception('Simulation tick failed')
    def stop(self): self.stop_event.set(); self.thread.join(timeout=20)
