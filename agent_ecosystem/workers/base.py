import time
from agent_ecosystem.runners.local_runner import LocalRunner


class Worker:
    def __init__(self, runner: LocalRunner):
        self.runner = runner
        self.is_running = False

    def start(self):
        self.is_running = True
        print("Worker started. Waiting for jobs...")
        # A simple polling loop (placeholder for real task queue like Celery/Redis)
        while self.is_running:
            time.sleep(1)

    def stop(self):
        self.is_running = False
        print("Worker stopped.")
