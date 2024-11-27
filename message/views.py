from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Logged-in user: Show user-specific and broadcast messages
            return Message.objects.filter(Q(receiver=user) | Q(receiver__isnull=True)).order_by('-timestamp')
        else:
            # Anonymous user: Show only broadcast messages
            return Message.objects.filter(receiver__isnull=True).order_by('-timestamp')

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(sender=self.request.user)
        else:
            serializer.save(sender=None)  # If sender is anonymous, set to None or a default value

    def retrieve(self, request, *args, **kwargs):
        """Fetch a single message."""
        instance = self.get_object()
        if request.user.is_authenticated and instance.receiver == request.user and not instance.is_read:
            instance.is_read = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Fetch all messages, with different behavior for logged-in and anonymous users."""
        queryset = self.get_queryset()
        if request.user.is_authenticated:
            # Mark unread messages as read for logged-in users
            queryset.filter(receiver=request.user, is_read=False).update(is_read=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
