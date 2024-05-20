from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="main-monitor"),
    path("entity_allocation", views.entity_allocation, name="entity_allocation"),
]
