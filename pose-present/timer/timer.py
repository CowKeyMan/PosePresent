"""
A big part of the algorithm deals with time, so a dedicated timer class
was created where the clients can set the maximum time,
and poll the timer to see if the time has passed
"""
import time


class Timer:
    def __init__(self, maximum_time: float) -> None:
        self.maximum_time = maximum_time
        self.end_time = time.time() - maximum_time
        self.active = False
        self.can_do = False

    def set_active(self, active: bool) -> None:
        if active is None:
            return
        if not self.active and active:
            self.end_time = time.time() + self.maximum_time
            self.can_do = True
        self.active = active

    def act(self) -> bool:
        result = time.time() > self.end_time and self.active and self.can_do
        if result:
            self.can_do = False
        return result
