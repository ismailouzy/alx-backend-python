from django.contrib import admin
from .models import Message, Notification, MessageHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'read', 'edited')
    list_filter = ('read', 'edited', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')
    raw_id_fields = ('sender', 'receiver', 'parent_message')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message__content')
    raw_id_fields = ('user', 'message')

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_at')
    search_fields = ('message__content',)
    raw_id_fields = ('message',)
