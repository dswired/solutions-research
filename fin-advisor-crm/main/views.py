from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.db.models import Q

from analytics.models import EntityTrend
from core.utils import get_current_time_greeting


def get_trend_history(request: HttpRequest):
    advisor_filter = Q(advisor__username=request.user.username) & Q(
        entity=request.user.username
    )
    if not request.POST.get("AsOfDate"):
        return EntityTrend.objects.filter(advisor_filter)
    date_filter = Q(date__lte=request.POST["AsOfDate"])
    return EntityTrend.objects.filter(advisor_filter & date_filter)


def get_summary_card_info(request: HttpRequest):
    today = datetime.today().strftime("%Y-%m-%d")
    trend = get_trend_history(request).latest("date")
    return {
        "value": trend.total_value,
        "gain": trend.total_gain,
        "return": "4.77",
        "fees": "29,000",
        "asof": request.POST.get("AsOfDate", today),
        "greeting": f"{get_current_time_greeting()} {request.user.first_name}!",
    }


@login_required(login_url="/authentication/login")
def index(request: HttpRequest):
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
    trend = get_trend_history(request)
    dates = [t.date for t in trend]
    values = [t.total_value for t in trend]
    config = {
        "type": "line",
        "data": {
            "labels": dates,
            "datasets": [
                {
                    "data": values,
                    "label": "Market Value",
                    "borderColor": "#4682B4",
                    "fill": True,
                }
            ],
        },
    }
    return JsonResponse(config)
