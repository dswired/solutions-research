from django.shortcuts import render
from django.http import JsonResponse

from .models import DailyPublicEquityTrades

from datetime import datetime


# Create your views here.
def get_summary_card_info():

    last_record = DailyPublicEquityTrades.objects.filter(ticker="AADS").latest(
        "trade_date"
    )

    return {
        "market_value": last_record.closing_price * last_record.total_shares_traded,
        "closing_price": last_record.closing_price,
        "total_return": last_record.price_change,
        "volume": last_record.total_shares_traded,
        "asof": datetime.today().strftime("%Y-%m-%d"),
        # "greeting": f"{get_current_time_greeting()} {request.user.first_name}!",
    }


def equities(request):
    context = get_summary_card_info()
    return render(request, "markets/equities.html", context=context)


def equity_trend(request):
    """Equity trend data endpoint"""
    per_ticker_data = DailyPublicEquityTrades.objects.filter(ticker="AADS")

    ticker_date = per_ticker_data.values_list("trade_date", flat=True)
    ticker_price = per_ticker_data.values_list("closing_price", flat=True)

    date_labels = []
    for date_item in ticker_date:
        date_labels.append(date_item)

    price_labels = []
    for price_item in ticker_price:
        price_labels.append(price_item)

    config = {
        "type": "line",
        "data": {
            "labels": date_labels,
            "datasets": [
                {
                    "data": price_labels,
                    "label": "Equity Price Trends",
                    "borderColor": "#4682B4",
                    "fill": True,
                }
            ],
        },
    }
    return JsonResponse(config)
