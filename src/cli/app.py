import os
import shutil
from typing import Annotated

import typer
from typer import Exit, Option
from rich import print

app = typer.Typer()

INIT_DIR = './.cag'


@app.command()
def init():
    """Creates a `.cag` directory to store cached files content."""
    if not os.path.exists(INIT_DIR):
        os.mkdir(INIT_DIR)
        print('[bold green]`.cag`[/bold green] directory was initialized.')
    else:
        print('[bold green]`.cag`[/bold green] directory is already initialized.')
        Exit(code=-1)


@app.command(
    name='deinit'
)
def de_init(
        force: Annotated[bool, Option(prompt=True, )]
):
    """Removes a `.cag` directory, with all cached content inside."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized.')
        Exit(code=-1)
    elif force:
        shutil.rmtree(INIT_DIR)
        print('[bold green]`.cag`[/bold green] directory was removed.')


if __name__ == '__main__':
    app()
