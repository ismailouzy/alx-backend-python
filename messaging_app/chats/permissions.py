from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it
    """
    
    def has_permission(self, request, view):
        # Allow only authenticated users
        if not request.user.is_authenticated:
            return False
            
        if view.action == 'list':
            return True
            
        return True

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant of the conversation
        if isinstance(obj, Conversation):
            return obj.participants.filter(id=request.user.id).exists()
        elif isinstance(obj, Message):
            return obj.conversation.participants.filter(id=request.user.id).exists()
        return False
