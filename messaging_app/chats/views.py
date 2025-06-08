from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        # Only show conversations where user is a participant
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])
        
        # Ensure current user is included
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

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    search_fields = ['content']

    def get_queryset(self):
        # Get conversation_id from query params if provided
        conversation_id = self.request.query_params.get('conversation_id')
        
        # Base queryset - only messages in conversations where user is participant
        queryset = Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')
        
        # Filter by conversation_id if provided
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
            
        return queryset

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        
        # Verify user is participant of the conversation
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You're not a participant of this conversation")
            
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        message = self.get_object()
        
        # Only allow sender to update their own messages
        if message.sender != self.request.user:
            raise PermissionDenied("You can only edit your own messages")
            
        serializer.save()

    def perform_destroy(self, instance):
        # Only allow sender or conversation participants to delete
        if instance.sender != self.request.user and \
           not instance.conversation.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You don't have permission to delete this message")
            
        instance.delete()
