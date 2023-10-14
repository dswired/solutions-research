from django.shortcuts import render
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, "fescripts/index.html")


def hello_world(request):
    if request.method == "POST":
        fn, ln = request.POST["first_name"], request.POST["last_name"]
        messages.success(request, f"Success: You entered {fn} and {ln}!")
    return render(request, "fescripts/hello-world.html")
