from pcs.init import initialize_object_nones
from pcs.argument_parser import parse_arguments
from dataclasses import dataclass
from pcs.pipeline import Pipeline
from model.model import Model
from systems.init import (
    init_model,
    init_stream,
    init_poses,
    init_states,
    init_presentation_master,
)
from systems.run import (
    get_next_frame,
    run_model,
    update_presentation,
    # show_keypoints_image,
)
from stream.stream import Stream
from utils.poses import Pose
from presentation_master.presentation_master import PresentationMaster
import numpy as np
import logging
import os

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL, format="%(asctime)s %(message)s")


@dataclass
class Data:
    # args:
    model_name_to_details: dict[str, dict[str, str | int]]
    model_name: str
    threshold: float
    stream_path: str | int
    presentation_path: str
    slide_number_start: int
    num_slides: int
    pose_to_action: dict[str, str]
    slide_to_state: dict[int, dict[str, dict | str]]
    keypoint_to_colour: dict[str, tuple[int, int, int]]
    flip_image: bool
    video_viewer_application_cmd: list[str]
    presentation_viewer_application_cmd: list[str]
    keypoint_pairs: list[tuple[str, str]]
    # dynamic:
    model: Model
    stream: Stream
    name_to_poses: dict[str, Pose]
    presentation_master: PresentationMaster
    current_frame: np.ndarray
    keypoints: dict[str, tuple[int, int]]


data = initialize_object_nones(Data)
parse_arguments(data)

init = Pipeline(
    data,
    [
        init_model,
        init_stream,
        init_poses,
        init_states,
        init_presentation_master,
    ],
)
run = Pipeline(
    data,
    [
        get_next_frame,
        run_model,
        update_presentation,
        # show_keypoints_image,  # for debugging
    ],
)


init.execute()
while True:
    run.execute()
