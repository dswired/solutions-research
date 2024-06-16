from datetime import datetime
from typing import List

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Client, Account
from analytics.models import EntityTrend
from core.utils import get_current_time_greeting


def get_trend_history(request: HttpRequest):
    advisor_filter = Q(advisor__username=request.user.username)

    if "selected_entity" in request.POST:
        entity_filter = Q(entity=request.POST["selected_entity"])
    elif "selected_client" in request.POST:
        entity_filter = Q(entity=request.POST["selected_client"])
    else:
        entity_filter = Q(entity=request.user.username)

    if not request.POST.get("AsOfDate"):
        final_filter = advisor_filter & entity_filter
    else:
        date_filter = Q(date__lte=request.POST["AsOfDate"])
        final_filter = advisor_filter & entity_filter & date_filter
    res = EntityTrend.objects.filter(final_filter)
    print(f"Trend: {[(t.date, t.total_value) for t in res]}")
    return res


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
def main_monitor(request: HttpRequest):
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


def entity_trend(request: HttpRequest):
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


def search(request: HttpRequest):
    # /search/?client=
    clientid = request.GET.get("client")
    payload = []

    if clientid:
        client_filter = Q(advisor__username=request.user.username) & Q(
            clientid__icontains=clientid
        )
        client_objects = Client.objects.filter(client_filter)

        for client_object in client_objects:
            payload.append(client_object.clientid)
    return JsonResponse({"status": 200, "data": payload})


def get_entity_dropdown_items(
    client: Client, accounts: List[Account], selected_entity: str = None
) -> list:
    """Helper function to retrieve all dropdown items and keep selected_entity as first item."""
    # client_name = client.name
    # if selected_entity:
    #     items = [selected_entity, f"{client_name} ({client.clientid})"]
    # else:
    #     items = [f"{client_name} ({client.clientid})"]

    # for account in accounts:
    #     entity_display_name = f"{client_name} | {account.account_name} ({account.accountid})"
    #     if entity_display_name == selected_entity:
    #         continue
    #     items.append(entity_display_name)
    items = [client.clientid]
    for account in accounts:
        if account.accountid == selected_entity:
            continue
        items.append(account.accountid)
    if selected_entity:
        items.insert(0, selected_entity)
    return items


def single_client(request):
    if request.method == "POST":

        if "selected_entity" in request.POST:
            selected_entity = request.POST["selected_entity"]
            try:
                account_object = Account.objects.get(accountid=selected_entity)
                client_object = Client.objects.get(clientid=account_object.clientid)
                account_objects = Account.objects.filter(clientid=client_object)
            except ObjectDoesNotExist:  # Client was selected. Not Account
                client_object = Client.objects.get(clientid=selected_entity)
                account_objects = Account.objects.filter(clientid=client_object)
            dropdown_items = get_entity_dropdown_items(
                client_object, account_objects, selected_entity
            )

        if "selected_client" in request.POST:
            selected_client = request.POST["selected_client"]
            client_object = Client.objects.get(clientid=selected_client)
            account_objects = Account.objects.filter(clientid=client_object)
            dropdown_items = get_entity_dropdown_items(client_object, account_objects)
        context = get_summary_card_info(request)
        context.update({"dropdown_items": dropdown_items})
        return render(request, "main/single-client.html", context=context)
