"""
User authentication forms for AusflugAgypten
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignUpForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'ihre@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Vorname'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Nachname'
        })
    )
    phone = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': '+49 123 456789'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Benutzername'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Passwort'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Passwort bestätigen'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Update profile with phone
            phone = self.cleaned_data.get('phone')
            if phone:
                user.profile.phone = phone
                user.profile.save()
        
        return user


class LoginForm(AuthenticationForm):
    """User login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Benutzername oder E-Mail'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Passwort'
        })
    )


class UserProfileForm(forms.ModelForm):
    """User profile edit form"""
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'input-field'})
    )
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'country', 'city', 'address', 'language_preference', 'newsletter_subscribed', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'input-field'}),
            'country': forms.TextInput(attrs={'class': 'input-field'}),
            'city': forms.TextInput(attrs={'class': 'input-field'}),
            'address': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'language_preference': forms.Select(attrs={'class': 'input-field'}),
            'newsletter_subscribed': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'avatar': forms.FileInput(attrs={'class': 'input-field'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add User fields to the form
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Update User model fields
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        
        if commit:
            user.save()
            profile.save()
        
        return profile

