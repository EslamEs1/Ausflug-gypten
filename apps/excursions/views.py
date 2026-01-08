"""
Views for Excursions app
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg
from .models import Excursion
from apps.tours.models import Location, TourCategory
from apps.core.models import PageHero


class ExcursionListView(ListView):
    """List all excursions with filtering"""
    model = Excursion
    template_name = 'excursions/index.html'
    context_object_name = 'excursions'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Excursion.objects.filter(is_active=True).select_related('location', 'category').prefetch_related('reviews')
        
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
        
        # Page Hero
        try:
            context['page_hero'] = PageHero.objects.filter(page='excursions', is_active=True).prefetch_related('badges').first()
        except PageHero.DoesNotExist:
            context['page_hero'] = None
        
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
        
        # Get approved reviews with rating > 3
        from apps.reviews.models import Review
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(Excursion)
        approved_reviews = Review.objects.filter(
            content_type=content_type,
            object_id=excursion.id,
            is_approved=True,
            rating__gt=3
        )
        
        context['reviews'] = approved_reviews[:10]
        
        # Calculate average rating and count (only reviews with rating > 3)
        if approved_reviews.exists():
            context['average_rating'] = approved_reviews.aggregate(Avg('rating'))['rating__avg']
            context['review_count'] = approved_reviews.count()
        else:
            context['average_rating'] = None
            context['review_count'] = 0
        
        # Add today's date for form min date
        from datetime import date
        context['today'] = date.today()
        
        return context


