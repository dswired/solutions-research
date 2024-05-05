from analytics.models import EntityTrend


def entity_trend(row: dict) -> None:
    EntityTrend.objects.get_or_create(
        entity=row["entityid"],
        date_opened=row["date"],
        total_portfolio_value=row["total_portfolio_value"],
    )
