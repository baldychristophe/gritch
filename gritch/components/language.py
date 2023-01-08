import json
import os

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static
from textual.widget import Widget

from rich.text import Text
from rich.style import Style

from gritch import ASSETS_DIR


class Language(Widget):

    language: str
    color: str

    def __init__(
        self,
        language: str,
        *,
        name=None,
        id=None,
        classes=None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.language = language
        self.color = self.get_language_color(language)

    @staticmethod
    def get_language_color(language):
        with open(os.path.join(ASSETS_DIR, 'github-colors.json')) as f:
            languages_to_colors = json.load(f)

        lang = languages_to_colors.get(language)
        if lang:
            return lang['color']
        return 'white'

    def compose(self) -> ComposeResult:
        if self.language:
            yield Container(
                # Render a colored full block "█"
                Static(Text("\u2588", style=Style(color=self.color)), classes='mr-1 w-auto'),
                Static(self.language, classes='w-auto'),
                classes='layout-horizontal',
            )
        else:
            yield Static("")
