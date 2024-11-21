from rest_framework import serializers
from .models import Alumni
from user.models import User  # Assuming your User model is in the 'user' app

class AlumniSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Alumni
        fields ='__all__'