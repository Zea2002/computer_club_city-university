from rest_framework import viewsets
from .models import Alumni
from .serializers import AlumniSerializer
from rest_framework import permissions

class AlumniViewSet(viewsets.ModelViewSet):
    queryset = Alumni.objects.all()
    serializer_class = AlumniSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
