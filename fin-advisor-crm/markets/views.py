from django.shortcuts import render

# Create your views here.
def equities(request):
    return render(request, "markets/equities.html")
