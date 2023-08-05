
import click
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def cli(file_path):
    console = Console()
    path_object = Path(file_path)
    text = path_object.read_text()
    markdown = Markdown(text)
    console.print(markdown)
