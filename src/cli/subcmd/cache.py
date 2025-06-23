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

            filetype = _check_file_type(path).lower()

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


def _check_file_type(path: Path) -> str:
    return from_file(path)
