from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search_address, name="search_address"),
    path("generate_addresses", views.generate_addresses, name="generate_addresses"),
]
