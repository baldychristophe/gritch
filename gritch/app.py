from textual.app import App, ComposeResult
from textual.widgets import Footer

from gritch.github import get_user
from gritch.user import User


class GritchApp(App):

    CSS_PATH = [
        'gritch.css', 'user.css',
        'styles/background.css', 'styles/color.css', 'styles/height.css', 'styles/layout.css',
        'styles/margin.css', 'styles/padding.css', 'styles/text.css', 'styles/width.css',
    ]
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        user = get_user()

        yield Footer()
        yield User(user=user)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
