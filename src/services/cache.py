from pathlib import Path

from magic import from_file
from cag.formatters.xml import XMLCtxFormatter
from cag.data_source import (
    TextDataSource,
    PDFDataSource,
    ImgOpenAIDataSource
)


def get_paths(path: Path):
    """Recursively get file paths from the directory and all subdirectories."""

    files = []
    for p in path.iterdir():
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(get_paths(p))

    return files


def store_context(
        path: Path,
        save_dir: Path,
        openai_api_key: str | None
):
    """Extracts, processes and stores provided files into cached ``Context``."""
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
                api_key=openai_api_key
            ).__call__(path)
        else:
            return

        formatter = XMLCtxFormatter(ctx)
        formatter.save(save_dir)
