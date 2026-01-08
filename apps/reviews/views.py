"""
Views for Reviews app
"""

from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import Review
from .forms import ReviewForm


class SubmitReviewView(View):
    """Handle review submission for any content type"""
    
    def post(self, request, *args, **kwargs):
        # Get content type and object ID from POST data
        content_type_id = request.POST.get('content_type_id')
        object_id = request.POST.get('object_id')
        
        if not content_type_id or not object_id:
            messages.error(request, "Ungültige Bewertungsanfrage.")
            return redirect('core:home')
        
        try:
            content_type = ContentType.objects.get_for_id(int(content_type_id))
            model_class = content_type.model_class()
            content_object = model_class.objects.get(id=int(object_id))
        except (ValueError, ContentType.DoesNotExist, AttributeError):
            messages.error(request, "Das bewertete Objekt wurde nicht gefunden.")
            return redirect('core:home')
        except model_class.DoesNotExist:
            messages.error(request, "Das bewertete Objekt wurde nicht gefunden.")
            return redirect('core:home')
        
        # Create form with content object
        form = ReviewForm(request.POST, content_object=content_object)
        
        if form.is_valid():
            review = form.save()
            messages.success(
                request,
                'Vielen Dank für Ihre Bewertung! '
                'Ihre Bewertung wird nach Überprüfung veröffentlicht.'
            )
            
            # Redirect back to the detail page
            if hasattr(content_object, 'get_absolute_url'):
                return redirect(content_object.get_absolute_url())
            else:
                return redirect('core:home')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
            
            # Redirect back to the detail page
            if hasattr(content_object, 'get_absolute_url'):
                return redirect(content_object.get_absolute_url())
            else:
                return redirect('core:home')

