import json
import os
from typing import Any

import click

CONFIG_DIR = ".config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

NOTES_DIR = "app_notes"


def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {"notes_directory": NOTES_DIR}
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def save_config(config: dict[str, Any]) -> None:
    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


@click.group()
@click.pass_context
def config(ctx: click.Context):
    """Configuration options."""
    pass


@config.command()
def create():
    """Create a new configuration."""
    config = load_config()

    save_config(config)
    click.echo("Configuration created!")


@config.command()
@click.pass_context
def show(ctx: click.Context):
    """Show current configuration."""

    click.echo(ctx.obj["author"])

    if not os.path.exists(CONFIG_FILE):
        click.echo("No configuration found.")
        return
    config = load_config()
    click.echo(f"Notes directory: {config.get('notes_directory', CONFIG_DIR)}")


@config.command()
@click.option("--notes-directory", "-n", type=click.Path(exists=True))
def update(notes_dir: str) -> None:
    """Setup the notes directory."""
    config = load_config()
    config["notes_directory"] = notes_dir

    save_config(config)
    click.echo(f"Notes directory set to '{notes_dir}'.")
