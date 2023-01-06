import os

from textual.app import ComposeResult

from textual.widgets import Static


class NavWidget(Static):
    def compose(self) -> ComposeResult:
        yield Static(f'Current directory: {os.getcwd()}')
