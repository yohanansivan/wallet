from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("wallet_app/", include("wallet_app.urls")),
    path("admin/", admin.site.urls),
]
