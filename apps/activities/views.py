"""
Views for Activities app
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q, Count, Avg
from django.utils import translation
from .models import Activity, ActivityCategory
from apps.core.models import PageHero


class ActivityListView(ListView):
    """List all activities with filtering"""
    model = Activity
    template_name = 'activities/index.html'
    context_object_name = 'activities'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Activity.objects.filter(is_active=True).select_related('category', 'location').prefetch_related('reviews')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by location
        location_slug = self.request.GET.get('location')
        if location_slug:
            queryset = queryset.filter(location__slug=location_slug)
        
        # Search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(title_en__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(description_en__icontains=search_query)
            )
        
        # Ordering
        ordering = self.request.GET.get('ordering', 'featured')
        if ordering == 'price_low':
            queryset = queryset.order_by('price')
        elif ordering == 'price_high':
            queryset = queryset.order_by('-price')
        elif ordering == 'popular':
            queryset = queryset.order_by('-is_popular', '-is_featured', 'title')
        else:  # featured/default
            queryset = queryset.order_by('-is_featured', '-is_popular', 'title')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories for filter
        context['categories'] = ActivityCategory.objects.filter(is_active=True).order_by('order', 'name')
        
        # Get featured categories for hero section
        context['featured_categories'] = ActivityCategory.objects.filter(
            is_active=True
        ).order_by('order', 'name')[:3]
        
        # Get featured activities
        context['featured_activities'] = Activity.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category', 'location')[:6]
        
        # Statistics
        context['total_activities'] = Activity.objects.filter(is_active=True).count()
        
        # Current filters
        context['current_category'] = self.request.GET.get('category', '')
        context['current_location'] = self.request.GET.get('location', '')
        context['current_search'] = self.request.GET.get('search', '')
        context['current_ordering'] = self.request.GET.get('ordering', 'featured')
        
        # Page Hero
        try:
            context['page_hero'] = PageHero.objects.filter(page='activities', is_active=True).prefetch_related('badges').first()
        except PageHero.DoesNotExist:
            context['page_hero'] = None
        
        return context


class ActivityDetailView(DetailView):
    """Activity detail page"""
    model = Activity
    template_name = 'activities/detail.html'
    context_object_name = 'activity'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Activity.objects.filter(is_active=True).select_related(
            'category', 'location'
        ).prefetch_related(
            'images',
            'inclusions',
            'important_info'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = self.object
        
        # Get related activities (same category)
        context['related_activities'] = Activity.objects.filter(
            category=activity.category,
            is_active=True
        ).exclude(id=activity.id).select_related('category', 'location')[:4]
        
        # Get all activities from same location
        if activity.location:
            context['location_activities'] = Activity.objects.filter(
                location=activity.location,
                is_active=True
            ).exclude(id=activity.id).select_related('category', 'location')[:3]
        
        # Get approved reviews with rating > 3
        from apps.reviews.models import Review
        from django.contrib.contenttypes.models import ContentType
        from django.db.models import Avg
        content_type = ContentType.objects.get_for_model(Activity)
        approved_reviews = Review.objects.filter(
            content_type=content_type,
            object_id=activity.id,
            is_approved=True,
            rating__gt=3
        )
        
        context['reviews'] = approved_reviews[:10]
        
        # Calculate average rating and count (only reviews with rating > 3)
        if approved_reviews.exists():
            context['average_rating'] = approved_reviews.aggregate(Avg('rating'))['rating__avg']
            context['total_reviews'] = approved_reviews.count()
        else:
            context['average_rating'] = None
            context['total_reviews'] = 0
        
        return context


