# cag_cli

`cag_cli` is a CLI application built with [Typer](https://typer.tiangolo.com/) and [cag](https://github.com/panalexeu/cag.git) — a simple Python library that allows loading various data sources into a unified XML format, which can be ingested into a model's context.

Model inference is not supported yet; however, loading PDFs, images (with OpenAI), and simple text files into the unified XML-text format is supported.

Here is a usage example (a directory with files was cached): 

[demo_cache_dir](./imgs/demo_cache_dir.gif)

Here is an example of image file caching. Befor runnnig commands `OPENAI_API_KEY` env was set up: 

[demo_cache_img_file](./imgs/demo_cache_img_file.gif)

## help

[cli_cag_help](./imgs/cli_cag_help.png)

[cli_cag_cache_help](./imgs/cli_cag_cache.png)

