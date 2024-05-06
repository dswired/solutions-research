from main.models import Account, Client
from core.utils import to_bool, to_nullable_date


def account(row: dict) -> None:
    client = Client.objects.get(clientid=row["clientid"])
    Account.objects.get_or_create(
        clientid=client,
        accountid=row["accountid"],
        account_name=row["name"],
        date_opened=row["open_date"],
        inception_date=to_nullable_date(row["inception_date"]),
        is_active=to_bool(row["active_status"]),
    )
