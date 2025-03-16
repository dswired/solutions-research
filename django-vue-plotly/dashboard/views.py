from django.shortcuts import render
import plotly.express as px

from .models import Ticker, HistoricalPrice
from datetime import datetime, timedelta, date

# Create your views here.

def generate_sparkline(price_data):
    """
    Creates a Plotly sparkline using px.line() and returns it as an HTML div.
    """
    if not price_data:
        return ""

    # Create DataFrame for Plotly Express
    df = {"index": list(range(len(price_data))), "price": price_data}

    # Generate Sparkline using px.line()
    fig = px.line(
        df,
        x="index",
        y="price",
    )

    # Format the chart (minimalist styling)
    fig.update_layout(
        template="none",
        plot_bgcolor="white",  # Match card background
        paper_bgcolor="white",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),  # Hide X-axis
        yaxis=dict(visible=False),  # Hide Y-axis
        height=50,  # Small height for sparkline effect
        width=140,  # Small width to fit inside card
    )
    fig.update_traces(line=dict(color="#1E3A8A"))
    # Convert the figure to an HTML div string
    sparkline_html = fig.to_html(full_html=False)

    return sparkline_html

def index(request):
    tickers = Ticker.objects.all().order_by("symbol")
    ticker_data = []

    selected_date = request.GET.get("selected_date")
    today = date.today()

    if selected_date:
        sdate = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        sdate = today

    ninety_days_ago = sdate - timedelta(days=90)

    for ticker in tickers:
        price_data_qs = HistoricalPrice.objects.filter(
            ticker=ticker,
            date__range=(ninety_days_ago, sdate)  # Get prices within this date range
        ).order_by('date').values_list('close_price', flat=True)

        if not price_data_qs.exists():
            continue

        price_data = list(price_data_qs)

        # Extract latest and old prices
        latest_price = price_data[-1] if price_data else None
        print(ticker.symbol, latest_price, sep="~")
        old_price = price_data[0] if price_data else None

        if latest_price and old_price and old_price != 0:
            percent_change = ((latest_price - old_price) / old_price) * 100
        else:
            percent_change = None
        
        # Prepare sparkline data
        sparkline = generate_sparkline(price_data)

        ticker_data.append({
            "symbol": ticker.symbol,
            "name": ticker.name,
            "latest_price": latest_price,
            "percent_change": percent_change,
            "sparkline": sparkline,
        })

    context = {
        "date_value": sdate.strftime("%Y-%m-%d"),
        "date_max": today.strftime("%Y-%m-%d"),
        "ticker_data": ticker_data
    }

    return render(request, 'dashboard/index.html', context)
