import time

import pyautogui
from state.state import State


class FastPresentationState(State):
    def do_action(self, action: str):
        pass

    def enter(
        self,
        *,
        number_of_slides: int,
        delay: float = 0.3,
        **_,
    ):
        delay = delay
        for i in range(number_of_slides):
            time.sleep(delay)
            pyautogui.press("space")
        self.master.change_state("presentation")
        self.master.states["presentation"].increase_slide_number(
            number_of_slides
        )
