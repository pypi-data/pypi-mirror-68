# Copyright (c) 2019 Toyota Research Institute
import abc
import time
import json
from monty.json import jsanitize, MontyDecoder
import threading

# This should probably be on a per-file basis
CHANNEL_THREAD_LOCK = threading.Lock()


class Channel(abc.ABC):
    @abc.abstractmethod
    def publish(self, event):
        pass


class FileChannel(Channel):
    def __init__(self, filename):
        self._filename = filename

    def publish(self, event):
        data = json.dumps(jsanitize(event, strict=True))
        CHANNEL_THREAD_LOCK.acquire()
        with open(self._filename, "a+") as f:
            f.write(data)
            f.write("\n")
        CHANNEL_THREAD_LOCK.release()

    def subscribe(self, iterations=None, poll_time=10):
        times_polled = 0
        with open(self._filename, "r+") as f:
            while True:
                raw = f.readline()
                while raw:
                    yield json.loads(raw, cls=MontyDecoder)
                    raw = f.readline()
                times_polled += 1
                if iterations is not None and times_polled > iterations:
                    break
                else:
                    time.sleep(poll_time)


class KinesisChannel(Channel):
    def __init__(self):
        raise NotImplementedError("Kinesis channel not yet implemented")

    def publish(self, event):
        raise NotImplementedError("Kinesis channel not yet implemented")
