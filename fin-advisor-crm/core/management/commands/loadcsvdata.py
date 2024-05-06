from csv import DictReader
from typing import Any

from django.core.management import BaseCommand, CommandError
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

    def write_message(self, msg: str, msg_type: str) -> None:
        msg_types = {
            "success": self.style.SUCCESS,
            "error": self.style.ERROR,
            "warning": self.style.WARNING,
        }
        mtype = msg_types[msg_type]
        self.stdout.write(mtype(msg))

    def handle(self, *args: Any, **options: Any) -> str | None:
        loader, file = options["loader"], options["file"]
        loader_func = getattr(loaders, loader)

        with open(file, "r") as csv_file:
            csv_ = DictReader(csv_file)
            for row in csv_:
                try:
                    loader_func(row)
                    msg = f"Sucessfully created {loader} object for {row}!"
                    self.write_message(msg, "success")
                except Exception as err:
                    msg = f"Failed to process row: {row} due to {err}"
                    self.write_message(msg, "error")

        msg = f"Sucessfully loaded {loader} data from {file}!"
        self.write_message(msg, "success")
