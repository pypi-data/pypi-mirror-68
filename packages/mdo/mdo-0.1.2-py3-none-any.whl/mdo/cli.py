from io import StringIO

import click
from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path
from subprocess import Popen, PIPE


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--width', '-w', default='130')
@click.option('--no-pager', is_flag=True, default=False)
def cli(file_path, width, no_pager):

    width = _get_width(width)
    string_io = StringIO()
    console = Console(file=string_io, width=width, force_terminal=True)

    markdown_text = _get_markdown_text(file_path)
    markdown_object = Markdown(markdown_text)

    console.print(markdown_object)

    text = string_io.getvalue()

    if no_pager:
        print(text)

    else:
        text_bytes = text.encode()
        less(text_bytes)


def _get_markdown_text(file_path):
    path_object = Path(file_path)
    text = path_object.read_text()
    return text


def _get_width(width):
    if width == 'full':
        return None
    else:
        return int(width)


def less(data):
    process = Popen(["less", "-R"], stdin=PIPE)

    process.stdin.write(data)
    process.communicate()
