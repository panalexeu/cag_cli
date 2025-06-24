import os.path
from pathlib import Path
from typing import Annotated

from typer import Typer, Exit, Option, progressbar
from rich import print

from src.cli.constants import INIT_DIR
from src.services.cache import get_paths, store_context

app = Typer(
    help='Processes and stores various data sources.'
)


@app.command()
def file(
        paths: list[Path],
        openai: Annotated[str, Option()] = os.environ.get('OPENAI_API_KEY')
):
    """Process locally stored files by providing paths."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized. '
              'Use [bold green]`init`[/bold green] command to initialize the directory.')
        raise Exit(code=-1)

    # process files in a progressbar
    with progressbar(paths, length=len(paths)) as paths:
        for path in paths:
            store_context(
                path,
                save_dir=Path(INIT_DIR),
                openai_api_key=openai
            )

    print('[bold green]`.cag`[/bold green] was updated with the new cached context. ')


@app.command()
def dir(
        path: Path,
        openai: Annotated[str, Option()] = os.environ.get('OPENAI_API_KEY')
):
    """Recursively process the dir by providing the path."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized. '
              'Use [bold green]`init`[/bold green] command to initialize the directory.')
        raise Exit(code=-1)

    if not path.is_dir():
        print(f'[bold green]`{path}`[/bold green] is not a directory.')
        raise Exit(code=-1)

    # recursively extract all files in the directory and subdirectories
    paths = get_paths(path)

    # process files in a progressbar
    with progressbar(paths, length=len(paths)) as paths:
        for path in paths:
            store_context(
                path,
                save_dir=Path(INIT_DIR),
                openai_api_key=openai
            )

    print('[bold green]`.cag`[/bold green] was updated with the new cached context. ')
