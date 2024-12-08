import cv2
import numpy as np
from state.state import State
from utils.visualisations import show_keypoints


class KeypointsState(State):
    def __init__(self, keypoint_to_colour: dict[str, tuple[int, int, int]]):
        self.winname = "Keypoints"
        self.keypoint_to_colour = keypoint_to_colour

    def update(
        self,
        *,
        frame: np.ndarray,
        keypoints: dict[str, tuple[int, int]],
        **_,
    ) -> None:
        show_keypoints(
            [keypoints],
            frame,
            "Keypoints",
            self.keypoint_to_colour,
            resize_dimensions=self.dimensions,
        )
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
        **_,
    ):
        self.dimensions = dimensions
        cv2.namedWindow(self.winname)
        cv2.moveWindow(self.winname, position[0], position[1])
        cv2.setWindowProperty(self.winname, cv2.WND_PROP_TOPMOST, 1)
