import numpy as np
import math
import time


class Pose:
    def __init__(self, bool_func, wait_time_first=0.1, wait_time_after=1.5):
        self.bool_func = bool_func
        self.timer_active = False
        self.time = time.time()
        self.wait_time_first = wait_time_first
        self.wait_time_after = wait_time_after

    def check_if_can_act(self, personwise_keypoints) -> bool:
        b = self.bool_func(personwise_keypoints)
        if b:
            if self.timer_active:
                if time.time() > self.time:
                    self.time = time.time() + self.wait_time_after
                    return True
            else:
                self.time = time.time() + self.wait_time_first
                self.timer_active = True
        if b is False:
            self.timer_active = False
        return False


def point(keypoints: dict[str, tuple[int, int]]) -> bool:
    if all(
        x in keypoints for x in "nose right_wrist right_elbow right_shoulder".split()
    ):
        rwr = keypoints["right_wrist"]
        nose = keypoints["nose"]
        relb = keypoints["right_elbow"]
        rsho = keypoints["right_shoulder"]
        arm_length = np.linalg.norm([rwr[0] - relb[0], rwr[1] - relb[1]])
        return bool(
            rwr[0] < nose[0]
            and relb[1] > rwr[1]
            and math.fabs(rwr[1] - rsho[1]) < arm_length / 2
        )
    return False


def bow(keypoints: dict[str, tuple[int, int]]) -> bool:
    nose = keypoints.get("nose", None)
    shoulder = keypoints.get("right_shoulder", keypoints.get("left_shoulder", None))
    if nose is not None and shoulder is not None:
        return nose[1] > shoulder[1]
    return False


def raise_elbow(keypoints: dict[str, tuple[int, int]]) -> bool:
    if all(x in keypoints for x in "left_elbow left_shoulder".split()):
        nose = keypoints["left_shoulder"]
        lelb = keypoints["left_elbow"]
        return nose[1] > lelb[1]
    return False
