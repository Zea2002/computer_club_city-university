from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlumniViewSet

# Create a router and register the AlumniViewSet
router = DefaultRouter()
router.register(r'alumni', AlumniViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Automatically includes the URLs for all the viewset actions
]
