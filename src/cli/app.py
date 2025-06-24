import os
import shutil
from typing import Annotated
from pathlib import Path

import typer
from typer import Exit, Option, Argument, progressbar
from rich import print

from cli.constants import INIT_DIR
from services.app import merge as invk_merge
from services.app import count_tokens
from .subcmd import cache

app = typer.Typer()
app.add_typer(cache.app, name='cache')


@app.command()
def init():
    """Creates a ``.cag`` directory to store cached files content."""
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
    """Removes a ``.cag`` directory, with all cached content inside."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized.')
        raise Exit(code=-1)

    if force:
        shutil.rmtree(INIT_DIR)
        print('[bold green]`.cag`[/bold green] directory was removed.')


@app.command()
def list():
    """Lists ``.cag`` directory content."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized.')
        raise Exit(code=-1)

    for path in Path(INIT_DIR).iterdir():
        if path.is_file():
            print(path.stem)


@app.command()
def merge():
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


@app.command()
def count(
        model: Annotated[str, Argument()] = 'gpt-4o-mini'
):
    """Counts token size of caches in ``.cag`` directory. Uses OpenAI tokenizer vocabulary."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized.')
        raise Exit(code=-1)

    token_dict = {}
    paths = [p for p in Path(INIT_DIR).iterdir()]
    with progressbar(paths, len(paths)) as paths:
        for path in paths:
            if path.is_file():
                token_dict[path.stem] = count_tokens(path, model)

    print(token_dict)


if __name__ == '__main__':
    app()
