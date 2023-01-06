import os

import click

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

    gritch_app = GritchApp()
    gritch_app.run()
