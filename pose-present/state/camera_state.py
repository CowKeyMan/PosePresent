import cv2
import numpy as np
from state.state import State


class CameraState(State):
    def __init__(self):
        self.winname = "Camera"

    def update(self, *, frame: np.ndarray, **_) -> None:
        frame = cv2.resize(frame, self.dimensions)
        cv2.imshow(self.winname, frame)
        cv2.waitKey(1)

    def do_action(self, action: str):
        if action == "next":
            self.close()

    def close(self):
        cv2.destroyAllWindows()
        self.master.change_state("presentation")
        self.master.do_action("next")

    def enter(
        self,
        *,
        position: tuple[int, int],
        dimensions: tuple[int, int],
        **kwargs,
    ):
        self.dimensions = dimensions
        cv2.namedWindow(self.winname)
        cv2.moveWindow(self.winname, position[0], position[1])
        cv2.setWindowProperty(self.winname, cv2.WND_PROP_TOPMOST, 1)
