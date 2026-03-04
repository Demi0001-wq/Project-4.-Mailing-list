from django import forms
from .models import Recipient, Message, Mailing

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ('full_name', 'email', 'comment')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body')

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('start_time', 'period', 'message', 'recipients')
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
