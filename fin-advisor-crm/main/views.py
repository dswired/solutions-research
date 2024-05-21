from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Client
from core.utils import get_current_time_greeting


def get_summary_card_info(request):
    return {
        "value": "423,177.23",
        "gain": "98,129",
        "return": "4.77",
        "fees": "29,000",
        "asof": datetime.today().strftime("%Y-%m-%d"),
        "greeting": f"{get_current_time_greeting()} {request.user.first_name}!",
    }


def entity_allocation(request):
    """Entity allocation data endpoint."""
    allocation_data = {
        "Alternatives": 1200,
        "Equities": 2790,
        "Fixed Income": 2970,
        "Other": 755,
    }
    return JsonResponse({"entity_allocation_data": allocation_data}, safe=False)


@login_required(login_url="/authentication/login")
def index(request):
    context = get_summary_card_info(request)
    return render(request, "main/monitor.html", context=context)
