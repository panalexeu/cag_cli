import os
from pathlib import Path
from shutil import rmtree

from cag.core.base import Context
from cag.formatters.xml import XMLCtxFormatter
from tiktoken import encoding_for_model


def merge(
        paths: list[Path],
        save_dir: Path
):
    """Merges all context in ``.cag`` dir into one."""

    # load and merge contexts into one
    ctxs = []
    for path in paths:
        ctx = XMLCtxFormatter.load(path).ctx
        ctxs.append(ctx)

    root_context = Context.merge(ctxs)

    # clear .cag directory
    for p in save_dir.iterdir():
        if p.is_dir():
            rmtree(p)
        elif p.is_file():
            os.remove(p)

    # store merged context
    formatter = XMLCtxFormatter(ctx=root_context)
    formatter.save(save_dir, name='root')


def count_tokens(
        path: Path,
        model: str
) -> int:
    enc = encoding_for_model(model)

    with open(path, 'r') as file:
        content = file.read()

    tokens = enc.encode(content)

    return len(tokens)
