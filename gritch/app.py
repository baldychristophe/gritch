from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from gritch.nav import NavWidget
from gritch.repositories import Repositories


class GritchApp(App):

    CSS_PATH = [
        'gritch.css', 'styles/background.css', 'styles/color.css', 'styles/height.css', 'styles/layout.css',
        'styles/margin.css', 'styles/text.css', 'styles/width.css',
    ]
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Footer()
        yield Repositories()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
