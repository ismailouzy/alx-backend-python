from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='sent_messages')
    conversation = models.ForeignKey(
            Conversation,
            on_delete=models.CASCADE,
            related_name='messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
