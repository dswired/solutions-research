from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest

from .models import Client
from core.utils import get_current_time_greeting

def get_current_trend_values(request):
    dte = request.asof
    ...


def get_summary_card_info(request:HttpRequest):
    return {
        "value": "423,177.23",
        "gain": "98,129",
        "return": "4.77",
        "fees": "29,000",
        "asof": datetime.today().strftime("%Y-%m-%d"),
        "greeting": f"{get_current_time_greeting()} {request.user.first_name}!",
    }


@login_required(login_url="/authentication/login")
def index(request: HttpRequest):
    print(dir(request))
    context = get_summary_card_info(request)
    return render(request, "main/monitor.html", context=context)


def entity_allocation(request: HttpRequest):
    """Entity allocation data endpoint."""
    data = {
        "Alternatives": 1250,
        "Equities": 2790,
        "Fixed Income": 2970,
        "Other": 755,
    }
    config = {
        "type": "doughnut",
        "data": {
            "labels": list(data.keys()),
            "datasets": [
                {
                    "label": "Portfolio Allocation",
                    "backgroundColor": [
                        "rgba(255, 99, 132, 0.5)",
                        "rgba(54, 162, 235, 0.5)",
                        "rgba(75, 192, 192, 0.5)",
                        "#e8c3b9",
                    ],
                    "data": list(data.values()),
                }
            ],
        },
    }
    return JsonResponse(config)


def entity_trend(request):
    """Entity trend data endpoint."""
    config = {
        "type": "line",
        "data": {
            "labels": [1500, 1600, 1700, 1750, 1800, 1850, 1900, 1950, 1999, 2050],
            "datasets": [
                {
                    "data": [282, 350, 411, 502, 635, 809, 947, 1402, 3700, 5267],
                    "label": "Market Value",
                    "borderColor": "#4682B4",
                    "fill": True,
                }
            ],
        },
    }
    return JsonResponse(config)
