"""
URL mapping for the client API.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from client import views


router = DefaultRouter()
router.register("clients", views.ClientViewSet)

app_name = "client"

urlpatterns = [
    path("", include(router.urls)),
]
