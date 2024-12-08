"""
The three item store allows the writer to keep writing, overriding itself.
However, as soon as the reader requests something, then the writer will start
ignoring that location from where the reader is reading from and writing in the
other 2 slots instead

The reader will always read from the last FULLY written location

This is primarily used in SkipFramesLiveStream and FfmpegSkipFramesLiveStream

A timeout is also added so that if a read request was given,
it can throw an error if it does not return for a certain amount of time.
For the timeout to be avoided, one can give a negative value for it
"""

import threading
import time


class ThreeItemStore:
    def __init__(
        self,
        first_item: object,
        reader_sleep_time: float,
        timeout: int = 30,  # HARDCODED
    ) -> None:
        self.reader_sleep_time: float = reader_sleep_time
        self.lock: threading.Lock = threading.Lock()
        self.store: list[object] = [first_item, first_item, first_item]
        self.previous_write_index: int = 0
        self.write_index: int = 1
        self.read_index: int = -1
        self.max_sleeps: float = timeout / reader_sleep_time
        self.sleeps: int = 0

    def write_next_item(self, item: object) -> None:
        self.store[self.write_index] = item
        self._set_next_write_position()

    def _set_next_write_position(self) -> None:
        with self.lock:
            self.previous_write_index = self.write_index
            while True:
                self.write_index = (self.write_index + 1) % len(self.store)
                if self.write_index != self.read_index:
                    break

    def read_last_written_item(self) -> object:
        while True:
            with self.lock:
                if self.read_index != self.previous_write_index:
                    self.sleeps = 0
                    self.read_index = self.previous_write_index
                    return self.store[self.read_index]
            time.sleep(self.reader_sleep_time)
            self.sleeps += 1
            if self.sleeps > self.max_sleeps and self.max_sleeps > 0:
                raise TimeoutError("Cannot read frame from stream")
