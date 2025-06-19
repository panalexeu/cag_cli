import typer
from pathlib import Path
from typer import Typer

app = typer.Typer(
    help='Processes and stores various data sources.'
)


@app.command()
def file(
        paths: list[Path]
):
    """Process locally stored files by providing paths."""
    breakpoint()
