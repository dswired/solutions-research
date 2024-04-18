from django.urls import path
from .views import index, equity_analytics

urlpatterns = [
    path("monitor/", index, name="main"),
    path("equity_analytics/", equity_analytics, name="equity_analytics"),  # Path for equity analytics page
    ]
