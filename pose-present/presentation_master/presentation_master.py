import logging

import numpy as np
from state.state import State
from utils.poses import Pose


class PresentationMaster:
    def __init__(
        self,
        states: dict[str, State],
        name_to_poses: dict[str, Pose],
        pose_to_action: dict[str, str],
    ):
        self.states = states
        self.state = states["presentation"]
        for state in states.values():
            state.set_master(self)
        self.name_to_poses = name_to_poses
        self.pose_to_action = pose_to_action

    def change_state(self, state_name: str, **kwargs) -> None:
        self.state = self.states[state_name]
        self.state.enter(**kwargs)

    def get_state(self) -> State:
        return self.state

    def update(
        self, frame: np.ndarray, keypoints: dict[str, tuple[float, float]]
    ):
        self.state.update(frame=frame, keypoints=keypoints)
        for pose_name, pose in self.name_to_poses.items():
            if pose.check_if_can_act(keypoints):
                logging.debug(f"Pose fulfilled: {pose_name}")
                self.do_action(self.pose_to_action[pose_name])

    def do_action(self, action: str):
        logging.debug(f"Executing action: {action}")
        self.state.do_action(action)
