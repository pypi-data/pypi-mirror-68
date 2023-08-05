import os

import click

URL_TEMPLATE = r"\e]8;;{url}\a{title}\e]8;;\a"

def info(msg):
    click.echo(click.wrap_text(msg))


def error(msg):
    click.echo(click.style(msg, fg="red"))


def paragraph(msg):
    click.echo(click.wrap_text(msg, initial_indent=" ", subsequent_indent=" "))


def link(url, title):
    string = URL_TEMPLATE.format(url=url, title=click.wrap_text(title))
    string = string.replace('"', "")
    os.system(f'echo -e "{string}"')
