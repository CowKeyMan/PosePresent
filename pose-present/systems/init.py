from model.model import Model
from presentation_master.presentation_master import PresentationMaster
from state.camera_state import CameraState
from state.presentation_state import PresentationState
from state.state import State
from state.application_state import ApplicationState
from stream.skip_frames_live_stream import SkipFramesLiveStream
from utils.poses import Pose, bow, point, raise_elbow
from state.keypoints_state import KeypointsState
from state.fast_presentation_state import FastPresentationState
from state.pose_state import PoseState


def init_model(
    model_name_to_details: dict[str, dict[str, str | int]],
    model_name: str,
    keypoint_to_colour: dict[str, tuple[int, int, int]],
    threshold: float,
) -> dict:
    path = model_name_to_details[model_name]['path']
    input_size = model_name_to_details[model_name]['input_size']
    assert isinstance(path, str)
    assert isinstance(input_size, int)
    keypoint_names = list(keypoint_to_colour.keys())
    model = Model(path, input_size, keypoint_names, threshold)
    return {"model": model}


def init_stream(stream_path: str | int) -> dict:
    return {"stream": SkipFramesLiveStream(stream_path)}


def init_poses():
    name_to_poses = {
        "point": Pose(point, 0.1, 1.5),
        "raise_elbow": Pose(raise_elbow, 0.1, 1.5),
        "bow": Pose(bow, 0.1, 1.5),
    }
    return {"name_to_poses": name_to_poses}


def init_states(
    presentation_viewer_application_cmd: list[str],
    presentation_path: str,
    slide_number_start: int,
    num_slides: int,
    slide_to_state: dict[int, dict[str, dict | str]],
    keypoint_to_colour: dict[str, tuple[int, int, int]],
    keypoint_pairs: list[tuple[str, str]]
):
    states = {
        "presentation": PresentationState(
            presentation_viewer_application_cmd,
            presentation_path,
            num_slides,
            slide_to_state,
            slide_number_start,
        ),
        "application": ApplicationState(),
        "camera": CameraState(),
        "keypoints": KeypointsState(keypoint_to_colour),
        "pose": PoseState(keypoint_to_colour, keypoint_pairs),
        "fast_presentation": FastPresentationState(),
    }
    return {"states": states}


def init_presentation_master(
    states: dict[str, State],
    name_to_poses: dict[str, Pose],
    pose_to_action: dict[str, str],
):
    return {
        "presentation_master": PresentationMaster(
            states, name_to_poses, pose_to_action
        )
    }
