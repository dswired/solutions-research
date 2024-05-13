from .views import LoginView, LogOutView
from django.urls import path

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogOutView.as_view(), name="logout"),
]
