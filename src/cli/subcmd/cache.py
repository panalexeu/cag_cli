import os.path
from pathlib import Path
from typing import Annotated

from magic import from_file
from typer import Typer, Exit, Argument, Option
from rich import print
from cag.formatters.xml import XMLCtxFormatter
from cag.data_source import (
    TextDataSource,
    PDFDataSource,
    ImgOpenAIDataSource
)

from src.cli.constants import INIT_DIR
from src.services.cache import _get_files

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

    # process files
    for path in paths:
        if path.is_file():

            filetype = from_file(path).lower()  # check file type

            # process text files
            if 'text' in filetype:
                ctx = TextDataSource().__call__(path)
            elif 'pdf' in filetype:
                ctx = PDFDataSource().__call__(path)
            elif 'image' in filetype:
                ctx = ImgOpenAIDataSource(
                    model='gpt-4.1-mini',
                    api_key=openai
                ).__call__(path)
            else:
                continue

            formatter = XMLCtxFormatter(ctx)
            formatter.__call__()
            formatter.save(Path(INIT_DIR))

    print('[bold green]`.cag`[/bold green] was updated with the new cached context. ')


@app.command()
def dir(
        path: Path
):
    """Recursively process the dir by providing the path."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized. '
              'Use [bold green]`init`[/bold green] command to initialize the directory.')
        raise Exit(code=-1)

    if not path.is_dir():
        print(f'[bold green]`{path}`[/bold green] is not a directory.')
        raise Exit(code=-1)

    # recursively extract all files in the directory
    files = _get_files(path)

