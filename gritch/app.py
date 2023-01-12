from textual import events
from textual.app import App, ComposeResult

from gritch.api_client import get_user
from gritch.messages import EnterDirectory, SwitchTab
from gritch.repository import RepositoryScreen
from gritch.user import UserScreen


class GritchApp(App):

    CSS_PATH = [
        'app.css',
        'styles/align.css', 'styles/background.css', 'styles/color.css', 'styles/dock.css', 'styles/height.css',
        'styles/layout.css', 'styles/margin.css', 'styles/overflow.css', 'styles/padding.css', 'styles/text.css',
        'styles/width.css',
    ]

    BINDINGS = [
        ('ctrl+q', 'quit', 'Exit'),
    ]

    def __init__(self):
        super().__init__()
        self.user = None

    def on_mount(self, event: events.Mount) -> None:
        user = get_user()
        self.user = user
        repos = user.get_repos()
        self.push_screen(RepositoryScreen(repository=repos[5], path=""))

        # self.install_screen(UserScreen(user=user, selected_tab_index=0), name='root')
        # self.push_screen('root')

    def on_enter_directory(self, event: EnterDirectory):
        self.push_screen(RepositoryScreen(repository=event.repository, path=event.path))

    def on_exit_directory(self):
        self.pop_screen()

    def on_switch_tab(self, event: SwitchTab):
        self.switch_screen(UserScreen(user=self.user, selected_tab_index=event.next_tab_index))
