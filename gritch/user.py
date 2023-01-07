from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Static
from textual.widget import Widget

from github import AuthenticatedUser, Repository

from . import api_client
from . import messages
from . import utils


class RepositoryPreview(Static):

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

    def on_click(self):
        self.log('Repository widget clicked')

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
                classes='width-1fr layout-horizontal',
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


class Repositories(Widget, can_focus=True):

    BINDINGS = [
        Binding('down', 'next_repository', 'Next', show=False),
        Binding('up', 'previous_repository', 'Previous', show=False),
        Binding('enter, right', 'enter_repository', 'Enter', show=False),
    ]

    def __init__(
        self,
        user: AuthenticatedUser,
        *,
        name=None,
        id=None,
        classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.selected_repository_index = 0
        self.user = user

    def action_next_repository(self) -> None:
        repository_widgets = self.query('RepositoryPreview')
        if len(repository_widgets) - 1 == self.selected_repository_index:
            # Do nothing if the last repository is already selected
            return

        repository_widgets[self.selected_repository_index].remove_class('selected-repository')
        self.selected_repository_index += 1
        repository_widgets[self.selected_repository_index].add_class('selected-repository')
        self.scroll_to_widget(repository_widgets[self.selected_repository_index])

    def action_previous_repository(self) -> None:
        repository_widgets = self.query('RepositoryPreview')
        if self.selected_repository_index == 0:
            # Do nothing if the first repository is already selected
            return

        repository_widgets[self.selected_repository_index].remove_class('selected-repository')
        self.selected_repository_index -= 1
        repository_widgets[self.selected_repository_index].add_class('selected-repository')
        self.scroll_to_widget(repository_widgets[self.selected_repository_index])

    def action_enter_repository(self) -> None:
        self.emit_no_wait(
            messages.EnterRepository(self, self.query('RepositoryPreview')[self.selected_repository_index].repository)
        )

    def on_mount(self, event: events.Mount):
        self.focus()

    def compose(self) -> ComposeResult:
        yield Static(f'Repositories', classes='mb-1')

        repos = [
            RepositoryPreview(
                repository=repository,
                classes='background-primary-darken-2 mb-1 mr-2 ml-2 px-2 border-repository',
            ) for repository in api_client.get_repositories(self.user)
        ]
        repos[self.selected_repository_index].add_class('selected-repository')
        yield Container(*repos, classes='px-4')


class UserScreen(Screen):
    def __init__(
        self,
        user: AuthenticatedUser,
        *,
        name=None,
        id=None,
        classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.user = user

    def compose(self) -> ComposeResult:
        yield Repositories(user=self.user)
