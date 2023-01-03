from textual.app import ComposeResult

from textual.containers import Vertical
from textual.widgets import Static
from textual.widget import Widget

from .github import get_repositories
from github import Repository


class RepositoryWidget(Static):
    repository: Repository

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
        yield Static(self.repository.name)
        if not self.repository.fork:
            yield Static(self.repository.language)
        else:
            yield Static(f'Forked from {self.repository.source.full_name}')
            yield Static(self.repository.source.language)


class Repositories(Widget):
    DEFAULT_CSS = """"""

    def compose(self) -> ComposeResult:
        yield Static(f'Repositories')

        repos = [
            RepositoryWidget(repository=repository) for repository in get_repositories()
        ]
        self.log(repos)
        yield Vertical(*repos)
