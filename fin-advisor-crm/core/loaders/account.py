from django.contrib.auth.models import User
from main.models import Account, Client


def account(row: dict) -> None:
    client = Client.objects.get(clientid=row["clientid"])
    Account.objects.get_or_create(
        clientid=client,
        accountid=row["accountid"],
        account_name=row["name"],
        date_opened=row["open_date"],
        inception_date=row["inception_date"],
        is_active=bool(row["active_status"]),
    )
