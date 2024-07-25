from typing import List

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.db.models import Q
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
    return EntityTrend.objects.filter(final_filter)


def get_allocation_info(request: HttpRequest):
    return {
        "Alternatives": 1250,
        "Equities": 2790,
        "Fixed Income": 2970,
        "Other": 755,
    }


def get_context_data(request: HttpRequest) -> dict:
    context = {"greeting": f"{get_current_time_greeting()} {request.user.first_name}!"}
    trend = get_trend_history(request)
    if trend:
        latest_trend = trend.latest("date")
        asof_date = latest_trend.date.strftime("%Y-%m-%d")
        latest_trend_values = {
            "asof": request.POST.get("AsOfDate", asof_date),
            "value": latest_trend.total_value,
            "gain": latest_trend.total_gain,
        }
    else:
        latest_trend_values = {
            "asof": request.POST.get("AsOfDate"),
            "value": "-",
            "gain": "-",
        }
    context.update(latest_trend_values)
    allocation = get_allocation_info(request)
    context.update(
        {
            "return": "4.77",
            "fees": "29,000",
            "trend": trend,
            "allocation": allocation,
        }
    )
    return context


@login_required(login_url="/authentication/login")
def main_monitor(request: HttpRequest):
    context = get_context_data(request)
    return render(request, "main/monitor.html", context=context)


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
    items = (
        [client.clientid] if selected_entity != client.clientid else [selected_entity]
    )
    for account in accounts:
        if account.accountid == selected_entity:
            continue
        items.append(account.accountid)
    if selected_entity and selected_entity != client.clientid:
        items.insert(0, selected_entity)
    return items


def single_client(request):
    # print(list(request.POST.items()))
    context = get_context_data(request)
    if request.method == "POST":
        if request.POST.get("selected_entity"):
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

        if request.POST.get("selected_client"):
            selected_client = request.POST["selected_client"]
            client_object = Client.objects.get(clientid=selected_client)
            account_objects = Account.objects.filter(clientid=client_object)
            dropdown_items = get_entity_dropdown_items(client_object, account_objects)
        context.update({"dropdown_items": dropdown_items})
        return render(request, "main/single-client.html", context=context)
