import os
import tempfile
import shutil

import click

from . import STARTING_DIRECTORY
from .app import GritchApp


@click.command()
@click.option("--dev", "dev", help="Enable development mode", is_flag=True)
def start(dev: bool):

    # Enable dev mode, taken from textual
    # see https://github.com/Textualize/textual/blob/main/src/textual/cli/cli.py
    from textual.features import parse_features
    features = set(parse_features(os.environ.get("TEXTUAL", "")))
    if dev:
        features.add("debug")
        features.add("devtools")

    os.environ["TEXTUAL"] = ",".join(sorted(features))

    with tempfile.TemporaryDirectory(prefix='gritch_') as temporary_dir:
        shutil.copytree('.', temporary_dir, dirs_exist_ok=True)
        try:
            os.chdir(temporary_dir)
            gritch_app = GritchApp()
            gritch_app.run()
        finally:
            os.chdir(STARTING_DIRECTORY)
