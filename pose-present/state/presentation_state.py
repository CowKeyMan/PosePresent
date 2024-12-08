import pyautogui
from state.state import State
from utils.applications import open_application


class PresentationState(State):
    def __init__(
        self,
        presentation_viewer_application_cmd: list[str],
        presentation_path: str,
        num_slides: int,
        slide_to_state: dict[int, dict[str, dict | str]],
        slide_number_start: int,
    ):
        self.presentation_path = presentation_path
        self.slide_number = slide_number_start
        self.slide_to_state = slide_to_state
        self.num_slides = num_slides
        self.switch_slide_after_begin = False
        open_application(
            presentation_viewer_application_cmd,
            presentation_path=presentation_path,
            slide_number_start=slide_number_start,
        )

    def do_action(self, action: str):
        if action == "next":
            self.next_slide()
        elif action == "previous":
            self.previous_slide()

    def next_slide(self):
        pyautogui.press("space")
        self.slide_number = min(self.slide_number + 1, self.num_slides)
        if self.slide_number in self.slide_to_state:
            state = self.slide_to_state[self.slide_number]['state']
            assert isinstance(state, str)
            params = self.slide_to_state[self.slide_number]['parameters']
            assert isinstance(params, dict)
            self.master.change_state(state, **params)

    def previous_slide(self):
        pyautogui.hotkey("shift", "space")
        self.slide_number = max(self.slide_number - 1, 1)

    def increase_slide_number(self, value: int):
        self.slide_number = min(self.slide_number + value, self.num_slides)
