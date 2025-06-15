from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Create notification when a new message is sent"""
    if created and not instance.parent_message:  # Only notify for parent messages
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            is_read=False
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log message history when content changes"""
    if instance.pk:  # Only for updates
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:  # Content changed
                MessageHistory.objects.create(
                    message=instance,
                    content=original.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass  # New instance

@receiver(post_delete, sender=User)
def delete_user_data(sender, instance, **kwargs):
    """Clean up related data when a user is deleted"""
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()
