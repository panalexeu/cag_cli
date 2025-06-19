import os.path
from pathlib import Path

from cag.data_source.text import TextDataSource
from cag.formatters.xml_format import XMLCtxFormatter
from magic import from_buffer
from typer import Typer, Exit

from src.cli.constants import INIT_DIR

app = Typer(
    help='Processes and stores various data sources.'
)


@app.command()
def file(
        paths: list[Path]
):
    """Process locally stored files by providing paths."""
    if not os.path.exists(INIT_DIR):
        print('[bold green]`.cag`[/bold green] directory is not initialized. '
              'Use [bold green]`init`[/bold green] command to initialize the directory.')
        raise Exit(code=-1)

    # process files
    for path in paths:
        if path.is_file():

            filetype = _check_file_type(path)

            # process text files
            if 'text' in filetype:
                ctx = TextDataSource().__call__(path)
                formatter = XMLCtxFormatter(ctx)
                formatter.__call__()
                formatter.save(Path(INIT_DIR))


def _check_file_type(path: str) -> str:
    with open(path, 'rb') as file:
        return from_buffer(file.read(2048))
