import os

from textual.app import ComposeResult

from textual.widgets import Static

from . import STARTING_DIRECTORY


class NavWidget(Static):
    def compose(self) -> ComposeResult:
        yield Static(STARTING_DIRECTORY)
        yield Static(f'Current directory: {os.getcwd()}')


