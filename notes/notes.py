import click

import commands

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context) -> None:
    "A simple not taking application."
    ctx.ensure_object(dict)
    author = "David Wiredu."
    ctx.obj["author"] = author


cli.add_command(commands.config)
cli.add_command(commands.crud)
