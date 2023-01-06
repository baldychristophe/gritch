from textual import events
from textual.app import App, ComposeResult
from textual.widgets import Footer

from gritch.api_client import get_user
from gritch.messages import EnterRepository
from gritch.repository import RepositoryScreen
from gritch.user import UserScreen


class GritchApp(App):

    CSS_PATH = [
        'gritch.css', 'user.css',
        'styles/background.css', 'styles/color.css', 'styles/height.css', 'styles/layout.css',
        'styles/margin.css', 'styles/padding.css', 'styles/text.css', 'styles/width.css',
    ]

    BINDINGS = [
        ('ctrl+q', 'quit', 'Exit'),
    ]

    SCREENS = {
        'repo': RepositoryScreen,
    }

    # def compose(self):
    #     user = get_user()
    #     yield UserScreen(user=user)

    def on_mount(self, event: events.Mount) -> None:
        user = get_user()
        self.install_screen(UserScreen(user=user), name='root')
        self.push_screen('root')

    def on_enter_repository(self, event: EnterRepository):
        self.push_screen(RepositoryScreen(event.repository))

    def on_exit_repository(self):
        self.pop_screen()
