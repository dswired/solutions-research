from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_monitor, name="main-monitor"),
    path("search/", views.search, name="search"),
    path("single-client", views.single_client, name="single-client"),
]
