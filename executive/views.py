from django.shortcuts import render
from rest_framework import viewsets
from .models import Executive
from .serializers import ExecutiveSerializer
from rest_framework.filters import SearchFilter
# Create your views here.

class ExecutiveViewSet(viewsets.ModelViewSet):
    queryset = Executive.objects.all()
    serializer_class = ExecutiveSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'designation']

