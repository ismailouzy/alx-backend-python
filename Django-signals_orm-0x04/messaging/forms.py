from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content', 'parent_message']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
