import cv2
import numpy as np
import seaborn as sns
from state.state import State
from utils.visualisations import show_full_pose


class PoseState(State):
    def __init__(
        self,
        keypoint_to_colour: dict[str, tuple[int, int, int]],
        keypoint_pairs: list[tuple[str, str]],
    ):
        self.winname = "Pose"
        self.keypoint_to_colour = keypoint_to_colour
        self.keypoint_pairs = keypoint_pairs
        self.colour_palette = np.array(sns.color_palette("husl", 8)) * 255

    def update(
        self, *, frame: np.ndarray, keypoints: dict[str, tuple[int, int]], **_
    ) -> None:
        show_full_pose(
            [keypoints],
            frame,
            self.keypoint_pairs,
            self.winname,
            self.keypoint_to_colour,
            self.colour_palette,
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
