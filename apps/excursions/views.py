"""
Views for Excursions app
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg
from .models import Excursion
from apps.tours.models import Location, TourCategory


class ExcursionListView(ListView):
    """List all excursions with filtering"""
    model = Excursion
    template_name = 'excursions/index.html'
    context_object_name = 'excursions'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Excursion.objects.filter(is_active=True).select_related('location', 'category')
        
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
        
        # Filter by rating (if reviews are implemented)
        min_rating = self.request.GET.get('rating')
        if min_rating:
            # This would need to join with reviews table
            pass
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(title_en__icontains=search) |
                Q(description__icontains=search) |
                Q(description_en__icontains=search)
            )
        
        # Sorting
        sort = self.request.GET.get('sort', 'featured')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'popular':
            queryset = queryset.order_by('-is_popular', '-is_bestseller', '-is_featured', 'title')
        elif sort == 'rating':
            # Would need to join with reviews
            queryset = queryset.order_by('-is_bestseller', '-is_popular', '-is_featured', 'title')
        else:  # featured/default
            queryset = queryset.order_by('-is_bestseller', '-is_popular', '-is_featured', 'title')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.filter(is_active=True).order_by('order', 'name')
        context['categories'] = TourCategory.objects.filter(is_active=True).order_by('order', 'name')
        
        # Current filters
        context['current_category'] = self.request.GET.get('category', '')
        context['current_location'] = self.request.GET.get('location', '')
        context['current_min_price'] = self.request.GET.get('min_price', '0')
        context['current_max_price'] = self.request.GET.get('max_price', '500')
        context['current_sort'] = self.request.GET.get('sort', 'featured')
        
        return context


class ExcursionDetailView(DetailView):
    """Excursion detail page"""
    model = Excursion
    template_name = 'excursions/detail.html'
    context_object_name = 'excursion'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Excursion.objects.filter(
            is_active=True
        ).select_related(
            'location', 'category'
        ).prefetch_related(
            'images', 'itinerary', 'inclusions'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        excursion = self.object
        
        # Get related excursions (same location)
        context['related_excursions'] = Excursion.objects.filter(
            is_active=True,
            location=excursion.location
        ).exclude(id=excursion.id).select_related('location', 'category')[:4]
        
        # Get excursions from same category
        if excursion.category:
            context['category_excursions'] = Excursion.objects.filter(
                category=excursion.category,
                is_active=True
            ).exclude(id=excursion.id).select_related('location', 'category')[:3]
        
        # Get approved reviews (if reviews app is implemented)
        context['reviews'] = []  # Placeholder - would use excursion.reviews.filter(is_approved=True)[:10]
        context['average_rating'] = excursion.average_rating
        context['review_count'] = excursion.review_count
        
        return context

