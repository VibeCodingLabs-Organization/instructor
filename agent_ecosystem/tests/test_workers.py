import threading
import time
from agent_ecosystem.runners.local_runner import LocalRunner
from agent_ecosystem.workers.base import Worker


def test_worker_start_stop():
    runner = LocalRunner()
    worker = Worker(runner)

    def run_worker():
        worker.start()

    thread = threading.Thread(target=run_worker)
    thread.start()

    time.sleep(0.1)
    assert worker.is_running

    worker.stop()
    thread.join(timeout=1.0)
    assert not worker.is_running
