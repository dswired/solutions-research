from django.contrib.auth.models import User

from main.models import Client
from core.utils import to_bool, to_nullable_date


def client(row: dict) -> None:
    advisor = User.objects.get(username=row["advisorid"])
    Client.objects.get_or_create(
        advisor=advisor,
        clientid=row["clientid"],
        name=row["name"],
        date_opened=row["date_opened"],
        inception_date=to_nullable_date(row["inception_date"]),
        client_type=row["client_type"].upper(),
        is_active=to_bool(row["is_active"]),
    )
