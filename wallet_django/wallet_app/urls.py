from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("generate_master/<str:coin>", views.generate_master, name="generate_master"),
    path("generate_address/<str:coin>", views.generate_address, name="generate_address"),
    path("list_address", views.list_address, name="list_address"),
    path("retrieve_address/<int:id>", views.retrieve_address, name="retrieve_address"),
]
