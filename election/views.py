import logging
from django.db.models import F, Max
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from .models import Candidate, Vote
from .serializers import CandidateSerializer, VoteSerializer

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

        try:
            Vote.objects.create(user=user, candidate=candidate, position=candidate.position)
            candidate.votes = F('votes') + 1
            candidate.save(update_fields=['votes'])
            candidate.refresh_from_db()  # Refresh the instance to update the votes count
        except Exception as e:
            logger.error(f"Error recording vote: {e}")
            return Response({"detail": "Error recording vote."}, status=500)

        return Response({"detail": "Vote successfully recorded."}, status=201)

    @action(detail=False, methods=['get'])
    def winners(self, request):
        try:
            # Find the maximum votes per position
            positions = Candidate.objects.values('position').annotate(max_votes=Max('votes'))

            winners_data = []
            
            for position in positions:
                position_name = position['position']
                max_votes = position['max_votes']

                # Fetch candidates who have the max votes for that position
                winners = Candidate.objects.filter(position=position_name, votes=max_votes)

                candidates_data = []
                for candidate in winners:
                    # Image URL
                    image_url = None
                    if candidate.user.image:
                        image_url = f"{settings.MEDIA_URL}{candidate.user.image.name}"

                    candidates_data.append({
                        "full_name": f"{candidate.user.first_name} {candidate.user.last_name}",
                        "manifesto": candidate.manifesto,
                        "votes": candidate.votes,
                        "image": image_url,  
                    })

                winners_data.append({
                    "position": position_name,
                    "candidates": candidates_data,
                })

            return Response(winners_data, status=200)

        except Exception as e:
            logger.error(f"Error fetching winners: {e}")
            return Response({"detail": "Error fetching winners."}, status=500)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    search_fields = ['user__first_name', 'user__last_name', 'candidate__position']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return self.queryset.none()
