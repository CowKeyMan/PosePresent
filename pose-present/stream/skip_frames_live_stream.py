"""
This class is an abstraction for opencv functions when
working with live streams. It inherits Stream

The name 'SkipFrames' comes from the fact that, using the ThreeItemStore,
we have a reader which is constantly reading from the live stream
(so that we do not buffer) and when we request a frame from this class,
we always get the latest frame from the live stream
(so there may be some frames in between which get skipped)
"""

import atexit
import threading

import numpy as np
from stream.stream import Stream
from thread_safe_stores.three_item_store import ThreeItemStore


class SkipFramesLiveStream(Stream):
    def __init__(
        self, stream_path: str | int, exit_if_cannot_read_frame: bool = True
    ) -> None:
        Stream.__init__(self, stream_path, exit_if_cannot_read_frame)
        self._setup_frame_store_parameters()
        self._start_reading()
        atexit.register(self.stop_reading)

    def _setup_frame_store_parameters(self) -> None:
        _, first_frame = self.stream.read()
        # It is unlikely the video will be more than 100fps,
        # hence this is a reasonable amount of time to sleep in between frames
        ten_milliseconds = 0.01  # HARDCODED
        self.frame_store: ThreeItemStore = ThreeItemStore(first_frame, ten_milliseconds)

    def _start_reading(self):
        self.read: bool = True
        # daemon = True instructs thread to stop when main stops
        self.read_thread: threading.Thread = threading.Thread(
            target=self._read_indefinitely, daemon=True
        )
        self.read_thread.start()

    def _read_indefinitely(self) -> None:
        while self.read:
            _, frame = self.stream.read()
            self._check_frame_was_read(frame)
            self.frame_store.write_next_item(frame)
        self.stream.release()

    def next_frame(self) -> np.ndarray:
        item = self.frame_store.read_last_written_item()
        assert isinstance(item, np.ndarray)
        return item

    def stop_reading(self) -> None:
        self.read = False
        self.read_thread.join()
