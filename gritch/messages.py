from textual.events import MessageTarget
from textual.message import Message

from github import Repository


class EnterRepository(Message, bubble=True):
    """Should be sent when entering a repository"""

    def __init__(self, sender: MessageTarget, repository: Repository) -> None:
        self.sender = sender
        self.repository = repository
        super().__init__(sender)


class ExitRepository(Message, bubble=True):
    pass
