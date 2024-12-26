import logging

from state.state import State
from utils.applications import open_application


class ApplicationState(State):
    def enter(self, **kwargs: str):
        application_cmd = kwargs.pop("application_cmd")
        assert isinstance(application_cmd, list)
        self.process = open_application(application_cmd, **kwargs)

    def do_action(self, action: str):
        if action == "next":
            self.close()

    def close(self):
        logging.debug("Closing application")
        self.process.kill()
        self.master.change_state("presentation")
        self.master.do_action("next")
