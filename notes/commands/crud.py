from datetime import datetime
import json
import os

import click


@click.group()
@click.pass_context
def crud(ctx: click.Context):
    """Note application crud operations."""
    pass


@crud.command()
@click.argument("title")
@click.option("--content", prompt=True, help="Note Content")
@click.option("--tags", help="tags.")
@click.pass_context
def create(ctx: click.Context, title: str, content: str, tags: str) -> None:
    """Create a new note."""
    # notes_directory = ctx.obj["notes_directory"]
    notes_directory = "app_notes"
    note_name = f"{title}.txt"
    note_file = os.path.join(notes_directory, note_name)
    if os.path.exists(note_file):
        click.echo(f"Note with title {title} already exists.")
        exit(1)

    note_data = {
        "content": content,
        "tags": tags.split(",") if tags else [],
        "created_at": datetime.now().isoformat(),
    }

    with open(note_file, "a") as file:
        json.dump(note_data, file)
    click.echo(f"Note {title} created.")


@crud.command()
@click.argument("title")
@click.pass_context
def read(ctx: click.Context, title: str) -> None:
    """Read a specific note."""
    author = ctx.obj["author"]
    notes_directory = "app_notes"
    note_name = f"{title}.txt"
    note_filename = os.path.join(notes_directory, note_name)
    if not os.path.exists(note_filename):
        click.echo(f"Note with title '{title}' does not exist.")
        exit(1)
    with open(note_filename, "r") as file:
        note_data = json.load(file)
    click.echo(f"Author: {note_data.get('author', author)}")
    click.echo(f"Title: {title}")
    click.echo(f"Tags: {', '.join(note_data['tags'])}")
    click.echo(f"Created At: {note_data['created_at']}")
    click.echo(f"Content:\n{note_data['content']}")
