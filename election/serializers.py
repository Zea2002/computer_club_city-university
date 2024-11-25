from rest_framework import serializers
from .models import Candidate, Vote

class CandidateSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    candidate_photo=serializers.SerializerMethodField()
    class Meta:
        model = Candidate
        fields = '__all__'
        
    def get_candidate_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_candidate_photo(self, obj):
        # Check if the user has an image file associated
        if obj.user.image and hasattr(obj.user.image, 'url'):
            return obj.user.image.url
        return None
class VoteSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()
    voter_name = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = '__all__'

    def get_candidate_name(self, obj):  # Fixed typo
        return f"{obj.candidate.user.first_name} {obj.candidate.user.last_name}"

    def get_voter_name(self, obj):
        return f"{obj.voter.first_name} {obj.voter.last_name}"
