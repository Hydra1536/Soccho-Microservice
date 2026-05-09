from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from users.api import router as users_router

api = NinjaAPI(title="Soccho Auth API", version="1.0.0")

api.add_router("/api/", users_router)

urlpatterns = [
    path("", api.urls),
    # Frontend calls: /auth/google/login
    # Wire social_django endpoints under the same /auth/ prefix.
    path("auth/", include("social_django.urls")),
    path("admin/", admin.site.urls),
]

