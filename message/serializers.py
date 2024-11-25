from rest_framework import serializers
from .models import Message
from user.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_image = serializers.ImageField(source='sender.image', read_only=True)
    receiver_name = serializers.CharField(source='receiver.first_name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp', 'is_read', 'sender_name', 'sender_image', 'receiver_name']
        read_only_fields = ['id', 'timestamp', 'is_read', 'sender_name', 'sender_image', 'receiver_name']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"