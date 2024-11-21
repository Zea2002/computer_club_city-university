from rest_framework import serializers
from .models import Activity, Participant, Result

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'user', 'activity', 'registered_at']

class ResultSerializer(serializers.ModelSerializer):
    participant = serializers.StringRelatedField()

    class Meta:
        model = Result
        fields = ['id', 'participant', 'rank', 'score', 'remarks']

class ActivitySerializer(serializers.ModelSerializer):
    participants_count = serializers.IntegerField(source='participants.count', read_only=True)
    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'description', 'activity_type', 
            'date', 'time', 'location', 'online_link', 
            'created_at', 'participants_count', 'results'
        ]
