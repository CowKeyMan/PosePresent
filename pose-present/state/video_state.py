import logging

from state.state import State
from utils.applications import open_application


class VideoState(State):
    def __init__(self, video_viewer_application_cmd: list[str]):
        self.video_viewer_application_cmd = video_viewer_application_cmd

    def enter(self, **kwargs: str):
        self.process = open_application(self.video_viewer_application_cmd, **kwargs)

    def do_action(self, action: str):
        if action == "next":
            self.close()

    def close(self):
        logging.debug("Closing video")
        self.process.kill()
        self.master.change_state("presentation")
        self.master.do_action("next")
