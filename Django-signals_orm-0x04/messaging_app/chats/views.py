from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from messaging.models import Message
from django.contrib.auth.decorators import login_required

@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_thread(request, message_id):
    # Get the parent message and prefetch all replies efficiently
    parent_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
                          .prefetch_related('replies__sender', 'replies__receiver'),
        pk=message_id
    )
    
    # Mark message as read when viewed
    if parent_message.receiver == request.user and not parent_message.read:
        parent_message.read = True
        parent_message.save()
    
    return render(request, 'chats/conversation_thread.html', {
        'parent_message': parent_message,
    })

@login_required
def inbox(request):
    # Get all unread messages for the current user
    unread_messages = Message.unread.for_user(request.user)
    
    # Get all conversations (parent messages only)
    conversations = Message.objects.filter(
        receiver=request.user,
        parent_message__isnull=True
    ).select_related('sender').prefetch_related('replies')
    
    return render(request, 'chats/inbox.html', {
        'unread_messages': unread_messages,
        'conversations': conversations,
    })
