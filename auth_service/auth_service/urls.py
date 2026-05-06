from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from users.api import router as users_router

api = NinjaAPI(title="Soccho Auth API", version="1.0.0")

api.add_router("/api/", users_router)

urlpatterns = [
    path("", api.urls),
    path("admin/", admin.site.urls),
]

