import cv2
import numpy as np
from model.model import Model
from presentation_master.presentation_master import PresentationMaster
from stream.stream import Stream
from utils.visualisations import show_keypoints


def get_next_frame(stream: Stream, flip_image: bool):
    frame = stream.next_frame()
    if flip_image:
        frame = cv2.flip(frame, 1)  # type: ignore
    return {"current_frame": frame}


def run_model(model: Model, current_frame: np.ndarray):
    return {"keypoints": model(current_frame)}


def update_presentation(
    presentation_master: PresentationMaster,
    current_frame: np.ndarray,
    keypoints: dict[str, tuple[float, float]],
):
    presentation_master.update(current_frame, keypoints)


def show_keypoints_image(
    keypoints: dict[str, tuple[int, int]],
    current_frame: np.ndarray,
    keypoint_to_colour: dict[str, tuple[int, int, int]],
):
    show_keypoints(
        [keypoints],
        current_frame,
        "Keypoints",
        keypoint_to_colour,
        resize_dimensions=None,
    )
    cv2.waitKey(1)
