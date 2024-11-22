from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, VoteViewSet, ElectionResultView, LiveVoteCountView

# Router setup
router = DefaultRouter()
router.register(r'candidates', CandidateViewSet, basename='candidate')
router.register(r'votes', VoteViewSet, basename='vote')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),  
    path('results/', ElectionResultView.as_view(), name='election-results'),  
    path('live-votes/', LiveVoteCountView.as_view(), name='live-vote-count'),  
]
