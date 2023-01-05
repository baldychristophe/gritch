from textual.app import ComposeResult

from textual.containers import Vertical, Container, Horizontal
from textual.widgets import Static
from textual.widget import Widget

from github import Repository

from .github import get_repositories
from . import utils


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

    def _get_repository_language(self):
        return (self.repository.source.language if self.repository.fork else self.repository.language) or ""

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Static(self.repository.name, classes='width-auto text-bold mr-3 primary-lighten-3'),
                Static(self.repository.visibility, classes='width-auto muted'),
                classes='width-1fr layout-horizontal',
            ),
            Container(
                Static(
                    f'Forked from {self.repository.source.full_name}' if self.repository.fork else "",
                    classes='text-right',
                ),
                classes='width-1fr layout-horizontal content-align',
            ),
            classes='layout-horizontal width-100',
        )
        yield Static(self.repository.description or "")

        yield Container(
            Static(self._get_repository_language(), classes='width-1fr'),
            Static(
                f'Updated on {utils.format_datetime(self.repository.updated_at)}',
                classes='width-1fr muted text-right',
            ),
            classes='layout-horizontal width-100',
        )


class Repositories(Widget):
    DEFAULT_CSS = """"""

    def compose(self) -> ComposeResult:
        yield Static(f'Repositories', classes='mb-1')

        repos = [
            RepositoryWidget(
                repository=repository,
                classes='background-primary-darken-1 mb-1 mr-2 ml-2 border-repository',
            ) for repository in get_repositories()
        ]
        self.log(repos)
        yield Container(*repos, classes='repo-container')
