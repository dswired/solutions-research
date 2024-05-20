from .views import LoginView, LogOutView
from django.urls import path

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout", LogOutView.as_view(), name="logout"),
]
