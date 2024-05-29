from django.urls import path
from . import views

urlpatterns = [
    path("", views.equities, name="equities"),
    path("equity_trend", views.equity_trend, name="equity_trend"),
]
