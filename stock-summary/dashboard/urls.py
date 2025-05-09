from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticker_summary_view, name='stock-summary'),
    path('test-dashboard', views.dashboard_view, name='dashboard'),
    path('update-chart/', views.update_line_chart, name='update_chart'),
]
