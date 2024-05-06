from django.urls import path
from markets import views

urlpatterns = [
    path("equities/", views.equities, name="equities")
]