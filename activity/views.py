from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Activity, Participant, Result
from .serializers import ActivitySerializer, ResultSerializer, ParticipantSerializer

class ActivityListCreateView(APIView):
    def get(self, request):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResultListView(APIView):
    def get(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id)
            results = Result.objects.filter(activity=activity)
            serializer = ResultSerializer(results, many=True)
            return Response({
                "activity": activity.name,
                "results": serializer.data
            })
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id)
            data = request.data.copy()
            data['activity'] = activity.id
            serializer = ResultSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)


class ParticipantListView(APIView):
    def get(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id)
            participants = activity.participants.all()  # Correct reference to 'participants'
            serializer = ParticipantSerializer(participants, many=True)
            return Response({
                "activity": activity.name,
                "participants": serializer.data
            })
        except Activity.DoesNotExist:
            return Response({"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Activity, Participant

class ParticipantRegistrationView(APIView):
    def post(self, request, activity_id):
        try:
            # Fetch the activity
            activity = Activity.objects.get(id=activity_id)

            # Check if the user is already registered
            if Participant.objects.filter(user=request.user, activity=activity).exists():
                return Response({"error": "You are already registered for this activity."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the participant registration for the logged-in user
            participant = Participant.objects.create(user=request.user, activity=activity)

            return Response({
                "message": "You have successfully registered for the activity."
            }, status=status.HTTP_201_CREATED)

        except Activity.DoesNotExist:
            return Response({"error": "Activity not found."}, status=status.HTTP_404_NOT_FOUND)
