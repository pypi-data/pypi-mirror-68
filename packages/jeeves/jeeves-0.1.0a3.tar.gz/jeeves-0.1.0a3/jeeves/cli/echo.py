import click


def title(string: str):
    click.echo(click.style(f"=== {string}", bold=True))


def info(string: str):
    symbol = click.style("(i)", fg="blue", bold=True)
    click.echo(f"{symbol} {string}")


def error(string: str):
    symbol = click.style("err", fg="red", bold=True)
    click.echo(f"{symbol} {string}")


def warning(string: str):
    symbol = click.style("[!]", fg="yellow", bold=True)
    click.echo(f"{symbol} {string}")


def success(string: str):
    symbol = click.style("ok!", fg="green", bold=True)
    click.echo(f"{symbol} {string}")
