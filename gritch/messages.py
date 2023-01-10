from textual.events import MessageTarget
from textual.message import Message

from github import Repository


class EnterDirectory(Message, bubble=True):
    """Should be sent when entering a directory tree"""

    def __init__(self, sender: MessageTarget, *, repository: Repository, path: str = "") -> None:
        self.sender = sender
        self.repository = repository
        self.path = path
        super().__init__(sender)


class ExitDirectory(Message, bubble=True):
    pass


class SwitchTab(Message, bubble=True):
    def __init__(self, sender: MessageTarget, *, next_tab_index: int) -> None:
        self.sender = sender
        self.next_tab_index = next_tab_index
        super().__init__(sender)
