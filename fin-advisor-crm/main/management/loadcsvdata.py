from typing import Any, Optional

from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ValidationError
from django.core.management.base import CommandParser

SUPPORTED_LOADERS = [
    "client",
    "account",
    "security",
    "entity_summary",
    "nav_history",
]


def is_supported_loader(loader: str) -> bool:
    return loader in SUPPORTED_LOADERS


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-f", "--file", help="Full path to loader file", type=str)
        parser.add_argument("-l", "--loader", help="Implemented loader")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        file, loader = options["file"], options["loader"]

        if not is_supported_loader(loader):
            raise ValidationError(f"Loader : {loader} not supported!")

        ldr = getattr()
