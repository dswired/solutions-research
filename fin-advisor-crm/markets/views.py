from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .models import DailyPublicEquityTrades

import json
import datetime
import requests
import locale


import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


EQUITY_DB_DATE_COL = "trade_date"
EQUITY_DB_PRICE_COL = "closing_price"


def format_currency(value):
    if value >= 1_000_000:
        return "GHS{:,.0f} M".format(value / 1_000_000)
    elif value >= 1_000:
        return "GHS{:,.0f} K".format(value / 1_000)
    else:
        return "GHS{:,.0f}".format(value)


def get_dropdown_data(request):
    data = DailyPublicEquityTrades.objects.all()  # Retrieve all objects from the model
    tickers = data.values_list("ticker", flat=True)
    unique_tickers = list(set(tickers))
    print("drop down func:", unique_tickers)
    return JsonResponse({'unique_tickers': unique_tickers})


def get_ticker_info(share_code):
    ticker_url = f'https://dev.kwayisi.org/apis/gse/equities/{share_code}'
    ticker_pull = requests.get(ticker_url)
    if ticker_pull.ok:
        return ticker_pull.json()
    else:
        raise ValueError


def get_ticker_info_basic(share_code):
    ticker_url = f"https://dev.kwayisi.org/apis/gse/live/{share_code}"
    ticker_pull = requests.get(ticker_url)
    if ticker_pull.ok:
        return ticker_pull.json()
    else:
        raise ValueError


def equity_trend_data_pull(
    selected_ticker, 
    as_of_date
    ):
    earliest_date = DailyPublicEquityTrades.objects.earliest("trade_date")
    start_date = earliest_date.trade_date.strftime("%Y-%m-%d")
    print("start date: ", earliest_date)
    selected_ticker_upper = selected_ticker.upper()
    if as_of_date:
        as_of_date = datetime.datetime.strptime(
            as_of_date, 
            "%Y-%m-%d"
        ).date()
        per_ticker_data = DailyPublicEquityTrades.objects.filter(
            ticker=selected_ticker_upper, 
            trade_date__range=[start_date, as_of_date]
        )
    else:
        per_ticker_data = DailyPublicEquityTrades.objects.filter(
            ticker=selected_ticker_upper
        )
    return per_ticker_data     


def equity_snap_data_pull(
    selected_ticker, 
    as_of_date
    ):
    if as_of_date:
        as_of_date = datetime.datetime.strptime(
            as_of_date, 
            "%Y-%m-%d"
        ).date()
        last_record = DailyPublicEquityTrades.objects.filter(
            ticker=selected_ticker, 
            trade_date=as_of_date
        ).latest("trade_date")
    else:
        last_record = DailyPublicEquityTrades.objects.filter(
            ticker=selected_ticker
        ).latest("trade_date")
    return last_record


def event_listener(request):
    if request.method == "POST":
        try:
            request_body = json.loads(request.body)
            selected_ticker = request_body.get("equityticker")
            as_of_date = request_body.get("asOfDate")
            print(f"Selected ticker: {selected_ticker} as of {as_of_date}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return selected_ticker, as_of_date


def series_data_processor(per_ticker_data, date_col, metric_col):
    ticker_date = per_ticker_data.values_list(date_col, flat=True)
    ticker_metric = per_ticker_data.values_list(metric_col, flat=True)

    date_labels = [date_item for date_item in ticker_date]
    metric_labels = [price_item for price_item in ticker_metric]
    return date_labels, metric_labels


@csrf_exempt
def get_summary_card_info(request: HttpRequest):
    # if request.method == "POST":
    #     try:
    #         request_body = json.loads(request.body)
    #         selected_ticker = request_body.get("equityticker")
    #         as_of_date = request_body.get("asOfDate")
    #         print(f"Selected ticker: {selected_ticker} as of {as_of_date}")
    #     except json.JSONDecodeError:
    #         return JsonResponse({"error": "Invalid JSON"}, status=400)
    selected_ticker, as_of_date = event_listener(request=request)        
    # real time gse data pull from kwaiysi
    selected_ticker_upper = selected_ticker.upper()
    ticker_info = get_ticker_info(share_code=selected_ticker_upper)
    ticker_info_basic = get_ticker_info_basic(share_code=selected_ticker_upper)

    # advance api call
    stock_name = ticker_info["name"]
    current_stock_price = ticker_info["price"]
    share_count = ticker_info["shares"]
    market_cap = ticker_info["capital"]
    sector = ticker_info["company"]["sector"]
    industry = ticker_info["company"]["industry"]

    # basic api call
    price_change = ticker_info_basic["change"]

    print("sector", sector)
    print("industry", industry)

    template = """Context: {question}
                """
    input_question = f"""You are a web application from which insights on Stocks is obtained. \n
                The user interface of this web application contains a list of stocks on the Ghana Stock Exchange. \n
                Each time a user of the web application selects a ticker, the equivalent company name,\
                sector, industry, and market capitalization is passed to you.  \n
                Your task is to generate a description that is displayed to the user. \n
                Note, the description provided is displayed on web application that is accessed \
                by professionals within the Ghanaian investment industry so the language should be professional \
                and not conversational. Also, no need to apologise, just get straight to the point. \n
                Your response should always begin with the company name provided to you. \n
                Company name: {stock_name} \n
                Company ticker: {ticker_info} \n
                Company sector: {sector} \n
                Company industry: {industry} \n
                Company market capitalization {market_cap}"""

    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3.1")
    chain = prompt | model
    ticker_description = chain.invoke({"question": f"{input_question}"})

    try:
        per_ticker_data = equity_trend_data_pull(
            selected_ticker=selected_ticker, 
            as_of_date=as_of_date
        )
        ticker_date = per_ticker_data.values_list("trade_date", flat=True)
        ticker_price = per_ticker_data.values_list("closing_price", flat=True)

        date_labels = [date_item for date_item in ticker_date]
        price_labels = [price_item for price_item in ticker_price]

    except DailyPublicEquityTrades.DoesNotExist:
        return JsonResponse({"error": "Ticker not found"}, status=404)

    trend_input_question = f"""You are a web application from which insights on Stocks is obtained. \n
                The user interface of this web application contains a list of stocks on the Ghana Stock Exchange. \n
                Each time a user of the web application selects a ticker, a corresponding list of stock prices \
                will be passed. Your task is to generate interesting insights of the trend based on the list \
                of prices. Bear in mind, the stock price is open source. \n
                Company name: {stock_name} \n
                Company sector: {sector} \n
                Company industry: {industry} \n
                Company historical prices: {price_labels} \n
                """

    trend_prompt = ChatPromptTemplate.from_template(template)
    equity_trend_description = chain.invoke({"question": f"{trend_input_question}"})

    data = {
        "market_value": format_currency(value=current_stock_price * share_count),
        "closing_price": "GHS{:,.2f}".format(current_stock_price),
        "price_change": "GHS{:,.2f}".format(price_change),
        "volume": "{:,.2f} M".format(share_count / 1_000_000),
        "tickerCommentary": ticker_description,
        "trendCommentary": equity_trend_description
    }
    return JsonResponse(data)
    # return JsonResponse({"error": "Invalid request method"}, status=405)




@csrf_exempt
def equity_trend(request):
    print("equity trend ticker: ")
    
    """Equity trend data endpoint"""
    selected_ticker, as_of_date = event_listener(request=request)

    per_ticker_data = equity_trend_data_pull(
        selected_ticker=selected_ticker, 
        as_of_date=as_of_date
    )

    date_labels, price_labels = series_data_processor(
        per_ticker_data=per_ticker_data, 
        date_col=EQUITY_DB_DATE_COL, 
        metric_col=EQUITY_DB_PRICE_COL
    )

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


def equities(request: HttpRequest):
    if request.method == "GET":
        # response = get_summary_card_info(request)
        print("Equities GET request: ")
        context = {}
        return render(request, "markets/equities.html", context=context)
    return render(request, "markets/equities.html", context=context)



