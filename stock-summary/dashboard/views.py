import random
import time
import pandas as pd
import plotly.express as px
from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from django.core.paginator import Paginator


from .models import Ticker, HistoricalPrice
from datetime import datetime, timedelta, date



def generate_stock_data():
    cached_data = cache.get("stock_data")
    if cached_data is not None:
        return cached_data

    # generate stock data if not already cached
    dates = pd.date_range(start="2004-01-01", periods=7300, freq="D")
    prices = [100]  # Starting price
    for _ in range(7299):
        prices.append(
            prices[-1] * (1 + random.uniform(-0.02, 0.02))
        )  # Simulating daily returns

    df = pd.DataFrame({"Date": dates, "Stock Price": prices})
    cache.set("stock_data", df, timeout=86400) # store in cache for 24 hours
    return df


def generate_chart(df, chart_type="market_prices"):
    if chart_type == "cumulative_returns":
        df["Cumulative Returns"] = df["Stock Price"].cumsum()
        y_axis = "Cumulative Returns"
        title = "Cumulative Returns Over 20 Years"
    else:
        y_axis = "Stock Price"
        title = "Stock Price Over 20 Years"

    fig = px.line(df, x="Date", y=y_axis, labels={y_axis: "Value ($)"}, title=title)

    # Apply None theme (transparent background)
    fig.update_layout(
        template="none",  # No background styling
        plot_bgcolor="white",  # Match card background
        paper_bgcolor="white",
        xaxis=dict(showgrid=False),  # No vertical grid
        yaxis=dict(
            showgrid=True, gridcolor="rgba(211, 211, 211, 0.3)"
        ),  # Faint horizontal grid
        font=dict(color="#1f2937"),  # Text color to match the card
    )

    # Set line color to Dark Blue
    fig.update_traces(line=dict(color="#1E3A8A"))  # Dark blue color

    return fig.to_html(full_html=False)



def generate_expense_data():
    months = pd.date_range(start="2024-01-01", periods=12, freq="ME").strftime("%b")
    revenue = [
        random.randint(50000, 200000) for _ in range(12)
    ]  # Simulating monthly revenue

    df = pd.DataFrame({"Month": months, "Expenses": revenue})
    return df


def generate_bar_chart():
    df = generate_expense_data()
    fig = px.bar(df, x="Month", y="Expenses", labels={"Expenses": "Expenses ($)"})

    fig.update_layout(
        template="none",  # No background styling
        plot_bgcolor="white",  # Match card background
        paper_bgcolor="white",
        xaxis=dict(showgrid=False),  # No vertical grid
        yaxis=dict(
            showgrid=True, gridcolor="rgba(211, 211, 211, 0.3)"
        ),  # Faint horizontal grid
        font=dict(color="#1f2937"),  # Text color to match the card
        hoverlabel=dict(
        bgcolor="white",  # Background color
        font_size=14,  # Font size
        font_family="Arial, sans-serif",  # Font family
        bordercolor="black",  # Border color
        namelength=-1  # Full name display
        )
    )

    fig.update_traces(marker_color="#1E3A8A")  # Use a professional blue color

    return fig.to_html(full_html=False)


def generate_pie_chart():
    categories = [
        "Salaries",
        "Rent",
        "Marketing",
        "Utilities",
        "Supplies",
        "Miscellaneous",
    ]
    expenses = [
        random.randint(10000, 50000) for _ in categories
    ]  # Simulated expense data

    df = pd.DataFrame({"Category": categories, "Amount": expenses})

    fig = px.pie(df, names="Category", values="Amount")

    fig.update_layout(
        template="none",  # No background styling
        font=dict(color="#1f2937"),  # Text color to match the card
    )

    return fig.to_html(full_html=False)


def generate_sales_data():
    customers = [
        "John Doe",
        "Jane Smith",
        "Michael Brown",
        "Emily Davis",
        "Chris Johnson",
    ]
    products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch"]

    sales_data = []
    for _ in range(100):  # Generate 100 random sales records
        sale = {
            "date": pd.Timestamp("2024-01-01") + pd.to_timedelta(random.randint(0, 364), unit="D"),
            "customer": random.choice(customers),
            "product": random.choice(products),
            "quantity": random.randint(1, 5),
            "total_price": round(random.uniform(100, 2000), 2),
            "change": round(random.uniform(-500, 500), 2)
        }
        sale["date"] = sale["date"].strftime('%Y-%m-%d')
        sales_data.append(sale)

    return sales_data

@login_required
@never_cache
def dashboard_view(request):
    df = generate_stock_data()
    latest_date = (
        df["Date"].max().strftime("%Y-%m-%d")
    )  # Ensure date picker shows last date
    chart_html = generate_chart(df)
    bar_chart_html = generate_bar_chart()
    pie_chart_html = generate_pie_chart()
    sales_data = generate_sales_data()
    data = {
        "line_chart": chart_html,
        "bar_chart": bar_chart_html,
        "pie_chart": pie_chart_html,
        "latest_date": latest_date,
        "sales_data": sales_data,
    }
    return render(request, "dashboard/dashboard.html", data)


def update_line_chart(request):
    chart_type = request.GET.get("chart_type", "market_prices")
    period_type = request.GET.get("period_type", "D")
    selected_date = request.GET["selected_date"]

    print(chart_type, period_type, selected_date, sep="~")

    df = generate_stock_data()
    df = df[df["Date"] <= selected_date]
    if period_type != "D":
        df.set_index("Date", inplace=True)
        df = df.resample(period_type).first().reset_index()

    chart_html = generate_chart(df, chart_type)
    return HttpResponse(chart_html)

# can use this to clear the cache.
# fyi request.session.flush()  # Clears all session data, including stock data
def clear_stock_request_cache(request):
    request.session.pop("stock_data", None)  # Removes stock data from session
    return HttpResponse("Stock data cache cleared.")

def clear_stock_cache():
    cache.delete("stock_data")  # Clears the cached stock data
    return HttpResponse("Stock data cache cleared.")



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

@login_required
@never_cache
def ticker_summary_view(request):
    time.sleep(2)
    tickers = Ticker.objects.all()
    ticker_data = []

    selected_date = request.GET.get("selected_date")
    today = date.today()
    if selected_date:
        # parse to a datetime.date
        sdate = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        sdate = today

    ninety_days_ago = sdate - timedelta(days=90)

    for ticker in tickers:
        price_data_qs = HistoricalPrice.objects.filter(
            ticker=ticker,
            date__range=(ninety_days_ago, sdate)  # Get prices within this date range
        ).order_by('date').values_list('close_price', flat=True)

        # Convert to list only if there is data
        price_data = list(price_data_qs) if price_data_qs.exists() else []

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
    
    # print(sdate, today, sep="~")

    #Implement pagination: 20 tickers per page
    paginator = Paginator(ticker_data, 20)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "today": today.strftime("%Y-%m-%d"),
        "selected_date": sdate.strftime("%Y-%m-%d"),
        "page_obj": page_obj
    }

    print("Page Number:", page_obj.number)
    print("Total Pages:", page_obj.paginator.num_pages)
    print("Has Next?", page_obj.has_next())
    print("Next Page #:", page_obj.next_page_number() if page_obj.has_next() else "N/A")

    
    # If request is from HTMX, return only the stock summary partial
    if "HX-Request" in request.headers:
        html = render_to_string("partials/stock-summary-cards.html", context)
        return HttpResponse(html)

    # Otherwise, return full page
    return render(request, "stock-summary/summary.html", context)