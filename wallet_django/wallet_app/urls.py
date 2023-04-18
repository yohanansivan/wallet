from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("testing/<str:coin>", views.testing, name="testing"),
]
