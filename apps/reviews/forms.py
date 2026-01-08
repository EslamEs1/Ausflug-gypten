"""
Review forms for AusflugAgypten
"""

from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Form for submitting reviews"""
    
    rating = forms.IntegerField(
        label="Bewertung",
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '1',
            'max': '5',
            'step': '1',
            'class': 'w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer',
            'id': 'ratingInput',
            'required': True,
        })
    )
    
    name = forms.CharField(
        label="Ihr Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Ihr Name',
            'required': True,
        })
    )
    
    email = forms.EmailField(
        label="E-Mail",
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'ihre@email.com',
            'required': True,
        })
    )
    
    title = forms.CharField(
        label="Titel der Bewertung",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'z.B. "Großartige Erfahrung!"',
            'required': True,
        })
    )
    
    comment = forms.CharField(
        label="Ihr Kommentar",
        widget=forms.Textarea(attrs={
            'class': 'input-field',
            'rows': 5,
            'placeholder': 'Teilen Sie Ihre Erfahrung mit anderen...',
            'required': True,
        })
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'name', 'email', 'title', 'comment']
    
    def __init__(self, *args, **kwargs):
        self.content_object = kwargs.pop('content_object', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        review = super().save(commit=False)
        if self.content_object:
            review.content_object = self.content_object
        review.is_approved = False  # Reviews need admin approval
        if commit:
            review.save()
        return review

