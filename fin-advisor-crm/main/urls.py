from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="main-monitor"),
    path("entity_allocation", views.entity_allocation, name="entity_allocation"),
    path("entity_trend", views.entity_trend, name="entity_trend"),
    path("search/", views.search, name="search"),
    path("single-client", views.single_client, name="main-singleclient"),
]
