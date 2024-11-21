from django.urls import path
from .views import ActivityListCreateView, ResultListView,ParticipantListView

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:activity_id>/results/', ResultListView.as_view(), name='result-list'),
    path('activities/<int:activity_id>/participants/', ParticipantListView.as_view(), name='participant-list'),
]
