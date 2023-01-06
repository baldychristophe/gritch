from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static
from textual.widget import Widget

from github import Repository

from . import messages


class RepositoryScreen(Screen):

    BINDINGS = [
        ('escape', 'exit_repository', 'Exit repository'),
    ]

    def __init__(
        self,
        repository: Repository,
        *,
        name=None,
        id=None,
        classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.repository = repository

    def compose(self) -> ComposeResult:
        yield Static(self.repository.full_name)

    def action_exit_repository(self):
        self.emit_no_wait(messages.ExitRepository(self))
