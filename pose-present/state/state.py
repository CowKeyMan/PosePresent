from abc import ABC, abstractmethod


class State(ABC):
    def enter(self, **_) -> None:
        return

    def set_master(self, master: "PresentationMaster"):  # type: ignore
        self.master = master

    def update(self, **_) -> None:
        return

    @abstractmethod
    def do_action(self, _action: str):
        return
