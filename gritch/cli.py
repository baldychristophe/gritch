import click

from .app import GritchApp


@click.command()
def start():
    

    gritch_app = GritchApp()
    gritch_app.run()
