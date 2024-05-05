from django.contrib.auth.models import User
from main.models import Client


def client(row: dict) -> None:
    advisor = User.objects.get(username=row["advisorid"])
    Client.objects.get_or_create(
        clientid=row["clientid"],
        name=row["name"],
        date_opened=row["date_opened"],
        client_type=row["client_type"].upper(),
        advisor=advisor,
        is_active=bool(row["active_status"]),
    )
