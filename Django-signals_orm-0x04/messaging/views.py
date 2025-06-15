from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from django.http import Http404
from .models import Message
from .forms import MessageForm

User = get_user_model()

@login_required
def inbox(request):
    # Get all unread messages for the current user with optimized queries
    unread_messages = Message.unread.unread_for_user(request.user)
    
    # Get all conversations with optimized queries
    conversations = Message.objects.filter(
        receiver=request.user,
        parent_message__isnull=True
    ).select_related('sender').prefetch_related('replies').only(
        'id', 'content', 'sender__username', 'timestamp'
    )
    
    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages,
        'conversations': conversations,
    })

@login_required
@cache_page(60)  # Cache for 60 seconds
def conversation_detail(request, message_id):
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver').only(
            'id', 'content', 'sender__username', 'receiver__username', 
            'timestamp', 'edited', 'edited_by__username'
        ),
        id=message_id
    )
    
    return render(request, 'messaging/conversation_detail.html', {
        'message': message
    })

@login_required
def create_message(request, receiver_id=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            if receiver_id:
                message.receiver = User.objects.get(id=receiver_id)
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    
    return render(request, 'messaging/create_message.html', {
        'form': form,
        'receiver_id': receiver_id
    })

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This will trigger the post_delete signal
        return redirect('home')
    return render(request, 'messaging/delete_user_confirm.html')
