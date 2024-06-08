from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="main-monitor"),
    path("entity_allocation", views.entity_allocation, name="entity_allocation"),
    path("entity_trend", views.entity_trend, name="entity_trend"),
    path("search_clients/", views.search_clients, name="search_clients"),
]
