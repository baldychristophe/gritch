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

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Static(self.icon, classes='w-auto mr-2'),
                Static(self.content_file.name, classes='w-auto'),
                classes='w-1fr layout-horizontal',
            ),
            Static(self.content_file.sha, classes='w-1fr text-right'),
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
        yield Container(*content_file_displays, classes='px-4')


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
        if self.mode == 'dir':
            yield Container(
                Static(self.repository.full_name, classes='mb-2'),
                Directory(repository=self.repository, content_files=self.path_content),
                classes='overflow-y-hidden', id='repository-content'
            )
        else:
            yield FileDisplay(content_file=self.path_content)
        yield Footer()

    def action_exit_repository(self):
        self.emit_no_wait(messages.ExitDirectory(self))
