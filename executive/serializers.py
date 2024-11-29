
from rest_framework import serializers
from .models import Executive
from user.serializers import UserSerializer

class ExecutiveSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(source='user.image', read_only=True)
    email=serializers.EmailField(source='user.email', read_only=True)
    username=serializers.CharField(source='user.username', read_only=True)
    phone=serializers.CharField(source='user.phone', read_only=True)
    full_name=serializers.SerializerMethodField()
    class Meta:
        model = Executive
        fields = ['id', 'username', 'designation', 'description', 'linkedIn', 'image', 'email', 'phone', 'full_name']
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

