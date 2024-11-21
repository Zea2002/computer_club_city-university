from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'location', 'start_date', 'start_time', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
