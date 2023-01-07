from textual import events
from textual.app import App, ComposeResult

from gritch.api_client import get_user
from gritch.messages import EnterDirectory
from gritch.repository import RepositoryScreen
from gritch.user import UserScreen


class GritchApp(App):

    CSS_PATH = [
        'app.css',
        'styles/background.css', 'styles/color.css', 'styles/height.css', 'styles/layout.css',
        'styles/margin.css', 'styles/overflow.css', 'styles/padding.css', 'styles/text.css', 'styles/width.css',
    ]

    BINDINGS = [
        ('ctrl+q', 'quit', 'Exit'),
    ]

    SCREENS = {
        'repo': RepositoryScreen,
    }

    def on_mount(self, event: events.Mount) -> None:
        user = get_user()
        self.install_screen(UserScreen(user=user), name='root')
        self.push_screen('root')

    def on_enter_directory(self, event: EnterDirectory):
        self.push_screen(RepositoryScreen(repository=event.repository, path=event.path))

    def on_exit_directory(self):
        self.pop_screen()
