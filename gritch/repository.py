from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Static
from textual.widget import Widget

from rich.syntax import Syntax

from github import Repository, ContentFile

from . import icons
from . import messages
from . import utils


class FileDisplay(Widget):
    content_file: ContentFile

    def __init__(
            self,
            *,
            content_file: ContentFile,
            name=None,
            id=None,
            classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.content_file = content_file
        self.syntax = Syntax(
            content_file.decoded_content.decode(),
            Syntax.guess_lexer(content_file.path),
            line_numbers=True,
        )

    def compose(self) -> ComposeResult:
        yield Container(Static(self.syntax))


class ContentFileDisplay(Static):
    def __init__(
        self,
        *,
        content_file: ContentFile,
        name=None,
        id=None,
        classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.content_file = content_file
        self.icon = icons.DIRECTORY if content_file.type == 'dir' else icons.FILE
        self.last_commit = self.content_file.repository.get_commits(path=self.content_file.path)[0]

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Static(self.icon, classes='w-auto mr-2'),
                Static(self.content_file.name, classes='w-auto'),
                classes='w-1fr layout-horizontal',
            ),
            Static(utils.truncate_commit_message(self.last_commit.commit.message, 30), classes='w-1fr'),
            Static(self.last_commit.commit.last_modified, classes='w-1fr text-right'),
            classes='layout-horizontal',
        )


class Directory(Widget, can_focus=True):

    repository: Repository
    path: str
    content_files: list[ContentFile]

    BINDINGS = [
        Binding('down', 'next_file', 'Next', show=False),
        Binding('up', 'previous_file', 'Previous', show=False),
        Binding('enter, right', 'enter_file', 'Enter', show=False),
    ]

    def __init__(
        self,
        *,
        repository: Repository,
        content_files: list[ContentFile],
        name=None,
        id=None,
        classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.repository = repository
        self.content_files = content_files
        self.last_commit = repository.get_commits()[0]
        # Sort files and directories
        self.content_files.sort(key=lambda x: x.type)
        self.selected_file_index = 0

    def action_next_file(self) -> None:
        content_file_displays = self.query('ContentFileDisplay')
        if len(content_file_displays) - 1 == self.selected_file_index:
            # Do nothing if the last repository is already selected
            return

        content_file_displays[self.selected_file_index].remove_class('highlight-background')
        self.selected_file_index += 1
        content_file_displays[self.selected_file_index].add_class('highlight-background')
        self.scroll_to_widget(content_file_displays[self.selected_file_index])

    def action_previous_file(self) -> None:
        content_file_displays = self.query('ContentFileDisplay')
        if self.selected_file_index == 0:
            # Do nothing if the last repository is already selected
            return

        content_file_displays[self.selected_file_index].remove_class('highlight-background')
        self.selected_file_index -= 1
        content_file_displays[self.selected_file_index].add_class('highlight-background')
        self.scroll_to_widget(content_file_displays[self.selected_file_index])

    def action_enter_file(self) -> None:
        selected_content_file = self.content_files[self.selected_file_index]
        self.emit_no_wait(messages.EnterDirectory(
            self,
            repository=self.repository,
            path=selected_content_file.path,
        ))

    def on_mount(self, event: events.Mount):
        self.focus()

    def compose(self) -> ComposeResult:
        content_file_displays = [
            ContentFileDisplay(content_file=content_file, classes='px-2 border-primary-background')
            for content_file in self.content_files
        ]
        content_file_displays[self.selected_file_index].add_class('highlight-background')
        yield Container(
            Static(icons.BRANCH, classes='w-auto mr-1'),
            Static(self.repository.default_branch, classes='w-auto mr-3'),
            Static(str(len(list(self.repository.get_branches()))), classes='w-auto text-bold mr-1'),
            Static('branches', classes='w-auto mr-3'),
            Static(icons.TAGS, classes='w-auto mr-1'),
            Static(str(len(list(self.repository.get_tags()))), classes='text-bold w-auto mr-1'),
            Static('tags', classes='w-auto mr-3'),
            Container(
                Static(self.repository.description, classes='text-right w-auto ah-right'),
                classes='ah-right w-auto text-right',
            ),
            classes='h-auto layout-horizontal px-2 border-primary-background panel-background mt-2',
        )
        yield Container(
            Static(self.last_commit.author.login, classes='text-bold w-1fr'),
            Static(utils.truncate_commit_message(self.last_commit.commit.message, 30), classes='w-1fr'),
            Static(self.last_commit.last_modified, classes='text-right w-1fr'),
            classes='h-auto layout-horizontal px-2 border-primary-background panel-background',
        )
        yield Container(*content_file_displays, classes='mt-1')


class PageTop(Widget):
    def __init__(
            self,
            *,
            repository: Repository,
            name=None,
            id=None,
            classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.repository = repository

    def compose(self) -> ComposeResult:

        yield Container(
            Static(self.repository.full_name, classes='w-auto mr-2'),
            Static(self.repository.visibility, classes='muted w-auto'),
            classes='layout-horizontal w-1fr'
        )
        if self.repository.fork:
            yield Container(
                Static('forked from', classes='mr-1 w-auto'),
                Static(self.repository.source.full_name, classes='w-auto secondary'),
                classes='layout-horizontal w-1fr text-center',
            )

        yield Container(
            # Watchers
            Static(icons.WATCHERS, classes='w-auto mr-1'),
            Static('watchers', classes='w-auto mr-1'),
            Static(str(self.repository.watchers_count), classes='w-auto text-bold mr-3'),
            # Forks
            Static(icons.FORKS, classes='w-auto mr-1'),
            Static('forks', classes='w-auto mr-1'),
            Static(
                str(self.repository.source.forks_count) if self.repository.fork else str(self.repository.fork_count),
                classes='w-auto text-bold mr-3',
            ),
            # Stars
            Static(icons.STARS, classes='w-auto mr-1'),
            Static('stars', classes='w-auto mr-1'),
            Static(str(self.repository.stargazers_count), classes='w-auto text-bold'),
            classes='layout-horizontal w-1fr ah-right',
        )


class RepositoryScreen(Screen):

    repository: Repository

    BINDINGS = [
        Binding('escape', 'exit_repository', 'Exit repository'),
    ]

    def __init__(
        self,
        *,
        repository: Repository,
        path: str,
        name=None,
        id=None,
        classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.repository = repository
        self.path = path
        self.path_content = repository.get_contents(path)
        if isinstance(self.path_content, list):
            self.mode = 'dir'
        else:
            self.mode = 'file'

    def compose(self) -> ComposeResult:
        yield PageTop(repository=self.repository, classes='dock-top h-auto p-1 layout-horizontal border-bottom-white')
        if self.mode == 'dir':
            yield Directory(repository=self.repository, content_files=self.path_content)
        else:
            yield FileDisplay(content_file=self.path_content)
        yield Footer()

    def action_exit_repository(self):
        self.emit_no_wait(messages.ExitDirectory(self))
