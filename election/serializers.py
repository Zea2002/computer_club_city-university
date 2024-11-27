from rest_framework import serializers
from .models import Candidate, Vote

class CandidateSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    image = serializers.ImageField(source='user.image', read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'position', 'full_name', 'image', 'votes', 'manifesto', 'user']
        read_only_fields = ['votes']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

   
class VoteSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = ['id','user', 'candidate', 'position', 'candidate_name','created_at']

    def get_candidate_name(self, obj):
        # Retrieve the full name of the candidate
        return f"{obj.candidate.user.first_name} {obj.candidate.user.last_name}"
