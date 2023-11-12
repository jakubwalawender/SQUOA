from django.urls import path, include
from .views import SystemLoginView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
]
