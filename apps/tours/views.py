"""
Views for Tours app
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg
from .models import Tour, Location, TourCategory


class TourListView(ListView):
    """List all tours with filtering"""
    model = Tour
    template_name = 'tours/tour_list.html'
    context_object_name = 'tours'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Tour.objects.filter(is_active=True).select_related('location', 'category').prefetch_related('reviews')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by location
        location_slug = self.request.GET.get('location')
        if location_slug:
            queryset = queryset.filter(location__slug=location_slug)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(title_en__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.filter(is_active=True)
        context['categories'] = TourCategory.objects.filter(is_active=True)
        return context


class TourDetailView(DetailView):
    """Tour detail page"""
    model = Tour
    template_name = 'tours/detail.html'
    context_object_name = 'tour'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Tour.objects.filter(
            is_active=True
        ).select_related(
            'location', 'category'
        ).prefetch_related(
            'images', 'itinerary', 'inclusions', 'reviews'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related tours
        context['related_tours'] = Tour.objects.filter(
            is_active=True,
            location=self.object.location
        ).exclude(id=self.object.id)[:3]
        
        # Get approved reviews with rating > 3
        context['reviews'] = self.object.reviews.filter(
            is_approved=True,
            rating__gt=3
        )[:10]
        
        return context


class FeaturedToursView(ListView):
    """Featured tours for homepage"""
    model = Tour
    template_name = 'tours/featured_tours.html'
    context_object_name = 'featured_tours'
    
    def get_queryset(self):
        return Tour.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('location', 'category')[:6]

