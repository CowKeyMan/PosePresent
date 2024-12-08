"""
A stream uses opencv's VideoCapture class to capture frame by frame
from a video or live stream. This class provides an abstration to
that opencv class to make it easier to work with
"""

from abc import ABC
from abc import abstractmethod
import numpy as np

import cv2


class Stream(ABC):
    def __init__(
        self, stream_path: str | int, exit_if_cannot_read_frame: bool = True
    ) -> None:
        self.stream: cv2.VideoCapture = cv2.VideoCapture(stream_path)
        self._check_stream_opened()
        _, frame = self.stream.read()
        self._check_frame_was_read(frame)
        self.exit_if_cannot_read_frame: bool = exit_if_cannot_read_frame

    def _check_stream_opened(self) -> None:
        if not self.stream.isOpened():
            raise ConnectionError("Cannot not open stream")

    def _check_frame_was_read(self, frame: np.ndarray | None):
        if frame is None and self.exit_if_cannot_read_frame:
            raise ValueError("Cannot read frame from stream, stream may be closed")

    @abstractmethod
    def next_frame(self) -> np.ndarray:
        raise NotImplementedError()

    def get_width(self) -> int:
        return int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))

    def get_height(self) -> int:
        return int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def stop_reading(self):
        self.stream.release()
