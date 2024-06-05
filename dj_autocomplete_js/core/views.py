from django.shortcuts import render
from django.http import JsonResponse

from faker import Faker
from .models import FakeAdress

fake = Faker()

# Create your views here.


def generate_addresses(request):
    for i in range(100):
        FakeAdress.objects.create(address=fake.address())
    return JsonResponse({"status": 200})


def home(request):
    return render(request, "index.html")

# search/?address=
def search_address(request):
    address = request.GET.get("address")
    payload = []
    if address:
        fake_address_objs = FakeAdress.objects.filter(address__startswith=address)
        payload = [x.address for x in fake_address_objs]
    return JsonResponse({"status": 200, "data": payload})
