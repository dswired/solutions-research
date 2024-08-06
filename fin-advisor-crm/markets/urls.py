from django.urls import path
from . import views

urlpatterns = [
    # path("", views.equity_view, name="equity_view"),
    # path("equity_view", views.equity_view, name="equity_view"),
    path("", views.equities, name="equities"),
    path("equity_trend", views.equity_trend, name="equity_trend"),
    path("get_dropdown_data", views.get_dropdown_data, name="get_dropdown_data"),
    path("trend_view_toggle", views.trend_view_toggle, name="trend_view_toggle"),
    path("get_summary_card_info", views.get_summary_card_info, name="get_summary_card_info"),
]
