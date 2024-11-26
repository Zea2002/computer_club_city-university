from rest_framework import viewsets
from django.db.models import Count, F,Max
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Candidate, Vote
from .serializers import CandidateSerializer, VoteSerializer
import logging

logger = logging.getLogger(__name__)

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    search_fields = ['user__first_name', 'user__last_name', 'position']

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        candidate = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response({"detail": "Authentication required to vote."}, status=401)

        if user.status != 'APPROVED':
            return Response({"detail": "You must be an approved club member to vote."}, status=403)

        if Vote.objects.filter(user=user, position=candidate.position).exists():
            return Response({"detail": "You have already voted for this position."}, status=400)

        Vote.objects.create(user=user, candidate=candidate, position=candidate.position)

        logger.debug(f"Before vote: {candidate.votes}")

        candidate.votes = F('votes') + 1
        candidate.save(update_fields=['votes'])

        logger.debug(f"After vote: {candidate.votes}")

        return Response({"detail": "Vote successfully recorded."}, status=201)

    @action(detail=False, methods=['get'])
    def winners(self, request):
        winners = {}
        votes = Vote.objects.values('candidate__position').annotate(vote_count=Count('id'))

        for vote in votes:
            position = vote['candidate__position']
            highest_votes = Candidate.objects.filter(position=position).aggregate(max_votes=Max('votes'))['max_votes']
            candidates = Candidate.objects.filter(position=position, votes=highest_votes)

            winners[position] = candidates

        winners_data = [
            {
                "position": position,
                "candidates": [
                    {
                        "full_name": f"{candidate.user.first_name} {candidate.user.last_name}",
                        "manifesto": candidate.manifesto,
                        "votes": candidate.votes,
                    }
                    for candidate in candidates
                ]
            }
            for position, candidates in winners.items()
        ]

        return Response(winners_data, status=200)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    search_fields = ['user__first_name', 'user__last_name', 'candidate__position']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return self.queryset.none()
