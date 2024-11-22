from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Candidate, Vote
from .serializers import CandidateSerializer, VoteSerializer

# Candidate ViewSet
class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

# Vote ViewSet
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

# Election Results View
class ElectionResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = {}
        for position, _ in Vote.position.field.choices:
            votes = Vote.objects.filter(position=position)
            candidate_votes = votes.values('candidate__user__username').annotate(vote_count=Count('id')).order_by('-vote_count')
            results[position] = list(candidate_votes)
        return Response(results)

# Live Vote Count View
class LiveVoteCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        live_results = {}
        for position, _ in Vote.position.field.choices:
            votes = Vote.objects.filter(position=position)
            candidate_votes = votes.values('candidate__user__username').annotate(vote_count=Count('id')).order_by('-vote_count')
            live_results[position] = list(candidate_votes)
        return Response(live_results)
