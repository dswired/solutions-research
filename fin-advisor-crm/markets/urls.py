from django.urls import path
from markets import views

urlpatterns = [
    path("", views.equities, name="equities")
]