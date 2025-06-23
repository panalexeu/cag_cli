import os
import shutil
from typing import Annotated
from pathlib import Path

import typer
from typer import Exit, Option
from rich import print

from src.cli.constants import INIT_DIR
from src.services.app import merge as invk_merge
from .subcmd import cache

app = typer.Typer()
app.add_typer(cache.app, name='cache')


@app.command()
def init():
    """Creates a `.cag` directory to store cached files content."""
    if not os.path.exists(INIT_DIR):
        os.mkdir(INIT_DIR)
        print('[bold green]`.cag`[/bold green] directory was initialized.')
        raise Exit()

    print('[bold green]`.cag`[/bold green] directory is already initialized.')
    raise Exit(code=-1)


@app.command(
    name='deinit'
)
def de_init(
        force: Annotated[bool, Option(prompt=True, )]
):
    """Removes a `.cag` directory, with all cached content inside."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized.')
        raise Exit(code=-1)

    if force:
        shutil.rmtree(INIT_DIR)
        print('[bold green]`.cag`[/bold green] directory was removed.')


@app.command(
    name='list'
)
def list():
    """Lists `.cag` directory content."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized.')
        raise Exit(code=-1)

    for path in Path(INIT_DIR).iterdir():
        if path.is_file():
            print(path.stem)


@app.command(
    name='merge'
)
def merge(

):
    """Merges ``Context``s of ``.cag`` directory into one."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized.')
        raise Exit(code=-1)

    paths = [p for p in Path(INIT_DIR).iterdir()]
    invk_merge(
        paths,
        Path(INIT_DIR)
    )

    print('Merge complete')


if __name__ == '__main__':
    app()
