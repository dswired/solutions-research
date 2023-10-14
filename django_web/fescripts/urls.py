from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="fescripts"),
    path("hello-world", views.hello_world, name="fescripts-hello-world"),
]
