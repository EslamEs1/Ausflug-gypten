"""
Forms for Core app
"""

from django import forms
from .models import ContactMessage, NewsletterSubscriber


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


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'flex-1 px-6 py-3 rounded-lg text-gray-800',
                'placeholder': 'Ihre E-Mail-Adresse',
                'required': True,
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('Diese E-Mail-Adresse ist bereits für den Newsletter angemeldet.')
        return email
    
    def save(self, commit=True):
        # If email already exists but is inactive, reactivate it
        email = self.cleaned_data['email']
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save()
        return subscriber


