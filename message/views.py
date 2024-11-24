from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Include both user-specific and broadcast messages
        return Message.objects.filter(Q(receiver=user) | Q(receiver__isnull=True)).order_by('-timestamp')

    def perform_create(self, serializer):
        # If no receiver is specified, it becomes a broadcast message
        serializer.save(sender=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Fetch a single message and mark it as read if applicable."""
        instance = self.get_object()
        if instance.receiver == request.user and not instance.is_read:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Fetch all messages for the logged-in user."""
        queryset = self.get_queryset()

        # Automatically mark all user-specific unread messages as read
        queryset.filter(receiver=request.user, is_read=False).update(is_read=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
