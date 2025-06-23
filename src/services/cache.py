from pathlib import Path


def _get_files(path: Path):
    """Recursively get files from the directory and all subdirectories."""

    files = []
    for p in path.iterdir():
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(_get_files(p))

    return files

def _extract_context(files: list[Path]):
    pass
