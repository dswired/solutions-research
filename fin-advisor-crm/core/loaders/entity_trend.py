from analytics.models import EntityTrend
from django.contrib.auth.models import User


def entity_trend(row: dict) -> None:
    advisor = User.objects.get(username=row["advisorid"])
    EntityTrend.objects.get_or_create(
        entity=row["entityid"],
        date=row["date"],
        total_value=row["total_value"],
        total_gain=row["total_gain"],
        advisor=advisor,
    )
