from markets.models import DailyPublicEquityTrades

def public_equities(row: dict) -> None:
    DailyPublicEquityTrades.objects.get_or_create(
        trade_date = row["trade_date"],
        ticker = row["ticker"],
        year_high = row["year_high"],
        year_low = row["year_low"],
        previous_closing_price = row["previous_closing_price"],
        opening_price = row["opening_price"],
        last_transaction_price = row["last_transaction_price"],
        closing_price = row["closing_price"],
        price_change = row["price_change"],
        closing_bid_price = row["closing_bid_price"],
        closing_offer_price = row["closing_offer_price"],
        total_shares_traded = row["total_shares_traded"],
        total_value_traded = row["total_value_traded"]
    )