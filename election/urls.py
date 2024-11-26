from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'candidates', CandidateViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
