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
