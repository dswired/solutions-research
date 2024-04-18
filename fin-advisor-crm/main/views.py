from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "main/monitor.html")


def equity_analytics(request):
    # Add your equity analytics logic here
    # context = {}  # Empty dictionary to store data for the template
    
    # Example - hypothetical data retrieval (replace with your actual logic)
    # equity_data = get_equity_data()  # Replace with your function to fetch data
    # context['equity_data'] = equity_data
    
    return render(request, "equity_analytics/equity_analytics.html")#, context)
