from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message
from .serializers import MessageSerializer
from django.db import models

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(models.Q(sender=user) | models.Q(receiver=user)).order_by('-timestamp')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Fetch a single message and mark it as read if the logged-in user is the receiver."""
        instance = self.get_object()
        if instance.receiver == request.user and not instance.is_read:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Fetch all messages and mark all received messages as read."""
        queryset = self.get_queryset()

        # Automatically mark unread messages as read
        queryset.filter(receiver=request.user, is_read=False).update(is_read=True)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)