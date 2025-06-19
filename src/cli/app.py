import os
import typer

from rich import print

app = typer.Typer()


@app.command()
def init():
    """Initializes .cag directory to store cache."""
    if not os.path.exists('./.cag'):
        os.mkdir('./.cag')
        print('.cag directory was initialized')


if __name__ == '__main__':
    app()
