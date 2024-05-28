from django.shortcuts import render

from .models import DailyPublicEquityTrades

from datetime import datetime

# Create your views here.
def get_summary_card_info():

    last_record = DailyPublicEquityTrades.objects.filter(ticker="AADS").latest("trade_date")
    
    date_labels = []
    per_ticker_data = DailyPublicEquityTrades.objects.filter(ticker="AADS")
    ticker_date = per_ticker_data.values_list("trade_date")
    for date_item in ticker_date:
        date_labels.append(date_item)

    return {
        "market_value": last_record.closing_price * last_record.total_shares_traded,
        "closing_price": last_record.closing_price,
        "total_return": last_record.price_change,
        "volume": last_record.total_shares_traded,
        "date_labels": date_labels,
        "asof": datetime.today().strftime("%Y-%m-%d"),
        # "greeting": f"{get_current_time_greeting()} {request.user.first_name}!",
    }


def equities(request):
    context = get_summary_card_info()
    return render(request, "markets/equities.html", context=context)