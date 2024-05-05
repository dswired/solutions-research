from csv import DictReader
from typing import Any

from django.core.management import BaseCommand
from django.core.management.base import CommandParser

from core import loaders


SUPPORTED_LOADERS = ["advisor", "client", "account", "entity_summary"]


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-f", "--file", help="csv file containing data.", type=str)

        parser.add_argument(
            "-l",
            "--loader",
            type=str,
            choices=SUPPORTED_LOADERS,
            help="Loader name as indicated in SUPPORTED_LOADERS.",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        loader, file = options["loader"], options["file"]

        loader = getattr(loaders, loader)

        self.stdout.write(
            self.style.SUCCESS(f"You entered the following arguments: {loader}, {file}")
        )
