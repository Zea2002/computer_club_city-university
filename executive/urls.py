# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExecutiveViewSet

router = DefaultRouter()
router.register(r'executives', ExecutiveViewSet, basename='executive')

urlpatterns = [
    path('', include(router.urls)),
]
