from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("wallet_app/", include("wallet_app.urls")),
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
]
