from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from .pagination import MessagePagination
from .filters import MessageFilter
import django_filters
from django.db.models import Q


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    search_fields = ['participants__username']

    def get_queryset(self):
        # Only show conversations where the user is a participant
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])

        # Ensure the current user is included in the conversation
        if request.user.id not in participants:
            participants.append(request.user.id)

        if len(participants) < 2:
            return Response(
                {"error": "At least two participants are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        # Only allow deletion if user is participant
        if instance.participants.filter(id=self.request.user.id).exists():
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "You are not a participant of this conversation"},
            status=status.HTTP_403_FORBIDDEN
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    search_fields = ['content']

    def get_queryset(self):
        # Only show messages from conversations the user is in
        queryset = super().get_queryset()
        return queryset.filter(
            Q(conversation__participants=self.request.user) |
            Q(sender=self.request.user)
        ).distinct()

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')

        # Check if user is participant of the conversation
        if not Conversation.objects.filter(
            id=conversation_id,
            participants=request.user
        ).exists():
            return Response(
                {"error": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        # Only allow deletion by sender or conversation participants
        if instance.sender != self.request.user and not instance.conversation.participants.filter(
            id=self.request.user.id
        ).exists():
            return Response(
                {"error": "You don't have permission to delete this message"},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
