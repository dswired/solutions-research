from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .models import DailyPublicEquityTrades
from core.utils import format_currency
from markets.utils import (DESCRIPTION_PROMPT, 
                           TREND_CHART_PROMPT, 
                           EQUITY_DB_DATE_COL, 
                           EQUITY_DB_PRICE_COL,
                           GSE_LIVE_PRICE_URL,
                           GSE_URL
                           )

import json
import datetime
import requests
import locale
import numpy as np
import pandas as pd

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def prompter(prompt):
    return prompt


def get_dropdown_data(request):
    data = DailyPublicEquityTrades.objects.all()  # Retrieve all objects from the model
    tickers = data.values_list("ticker", flat=True)
    unique_tickers = list(set(tickers))
    print("drop down func:", unique_tickers)
    return JsonResponse({'unique_tickers': unique_tickers})


def trend_view_toggle(request):
    toggle_options = ["Prices", "Volume"]
    return JsonResponse({"trend_toggle": toggle_options})


def get_ticker_info(url, share_code):
    ticker_url = f'{url}/{share_code}'
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
        as_of_date = datetime.datetime.strptime(as_of_date, "%Y-%m-%d").date()
        per_ticker_data = DailyPublicEquityTrades.objects.filter(
            ticker=selected_ticker_upper, 
            trade_date__range=[start_date, as_of_date]
        )
    else:
        per_ticker_data = DailyPublicEquityTrades.objects.filter(ticker=selected_ticker_upper)
    return per_ticker_data     


def event_listener(request):
    if request.method == "POST":
        try:
            request_body = json.loads(request.body)
            selected_ticker = request_body.get("equityticker")
            as_of_date = request_body.get("asOfDate")
            trend_type = request_body.get("trendtoggle")
            print(f"Selected ticker: {selected_ticker} as of {as_of_date} for {trend_type}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return selected_ticker, as_of_date, trend_type


def series_data_processor(per_ticker_data, date_col, metric_col):
    ticker_date = per_ticker_data.values_list(date_col, flat=True)
    ticker_metric = per_ticker_data.values_list(metric_col, flat=True)

    date_labels = [date_item for date_item in ticker_date]
    metric_labels = [price_item for price_item in ticker_metric]
    return date_labels, metric_labels


@csrf_exempt
def get_summary_card_info(request: HttpRequest):
    print("get_summary_card_info")
    selected_ticker, as_of_date, trend_type = event_listener(request=request)        
    
    # real time gse data pull from kwaiysi
    selected_ticker_upper = selected_ticker.upper()
    
    ticker_info = get_ticker_info(url=GSE_URL, 
                                  share_code=selected_ticker_upper)
    
    ticker_info_basic = get_ticker_info(url=GSE_LIVE_PRICE_URL,
                                              share_code=selected_ticker_upper)

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

    template = """Context: {question}"""

    input_question = DESCRIPTION_PROMPT.format(stock_name, 
                                               ticker_info,
                                               sector,
                                               industry,
                                               market_cap)

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

        mean_price = round(np.mean(price_labels), 2)
        median_price = round(np.median(price_labels), 2)
        price_std = round(np.std(price_labels), 2)
        min_price = round(np.min(price_labels), 2)
        max_price = round(np.max(price_labels), 2)
        inception_price = price_labels[0]
        inception_date = date_labels[0]

    except DailyPublicEquityTrades.DoesNotExist:
        return JsonResponse({"error": "Ticker not found"}, status=404)

    trend_input_question = TREND_CHART_PROMPT.format(stock_name, 
                                               current_stock_price, 
                                               mean_price, 
                                               median_price,
                                               price_std,
                                               min_price,
                                               max_price,
                                               inception_price,
                                               inception_date)

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


@csrf_exempt
def equity_trend(request):
    """Equity trend data endpoint"""
    
    selected_ticker, as_of_date, trend_type = event_listener(request=request)
    print("equity_trend", trend_type)

    per_ticker_data = equity_trend_data_pull(
        selected_ticker=selected_ticker, 
        as_of_date=as_of_date
    )
    metric_mapping = {"volume" : "total_shares_traded", "prices": "closing_price"}
    db_metric_column = metric_mapping[trend_type]

    date_labels, price_labels = series_data_processor(
        per_ticker_data=per_ticker_data, 
        date_col=EQUITY_DB_DATE_COL, 
        metric_col=db_metric_column
    )

    trend_graph_data = pd.DataFrame({"Date" : date_labels, "Metrics": price_labels})
    trend_graph_data["Date"] = pd.to_datetime(trend_graph_data["Date"])
    trend_graph_data.set_index("Date", inplace=True)

    if trend_type == "volume":
        trend_graph_data_annual = trend_graph_data.resample("Q").sum()
    else:
        trend_graph_data_annual = trend_graph_data.resample("Q").mean()

    date_labels = list(trend_graph_data_annual.index.date)
    price_labels = list(trend_graph_data_annual.Metrics)

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



