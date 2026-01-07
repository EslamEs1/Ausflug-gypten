"""
Forms for Core app
"""

from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Ihr vollständiger Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-field',
                'placeholder': 'ihre@email.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': '+49 ',
            }),
            'subject': forms.Select(attrs={
                'class': 'input-field',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 5,
                'placeholder': 'Ihre Nachricht...',
                'required': True,
            }),
        }
        labels = {
            'name': 'Name *',
            'email': 'E-Mail *',
            'phone': 'Telefon',
            'subject': 'Betreff *',
            'message': 'Nachricht *',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].empty_label = 'Bitte wählen...'

