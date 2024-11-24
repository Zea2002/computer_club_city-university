from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Save the contact message."""
        serializer.save()
