"""
Template tags for Reviews app
"""

from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def content_type_id(obj):
    """Get the ContentType ID for an object"""
    if obj:
        return ContentType.objects.get_for_model(obj).id
    return None

