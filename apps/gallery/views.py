"""
Views for Gallery app
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import GalleryImage, GalleryCategory


class GalleryListView(ListView):
    """List all gallery images with filtering"""
    model = GalleryImage
    template_name = 'gallery/index.html'
    context_object_name = 'images'
    paginate_by = 24
    
    def get_queryset(self):
        queryset = GalleryImage.objects.filter(is_active=True).select_related(
            'category', 'location'
        )
        
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
        ordering = self.request.GET.get('ordering', 'order')
        if ordering == 'newest':
            queryset = queryset.order_by('-created_at')
        elif ordering == 'oldest':
            queryset = queryset.order_by('created_at')
        elif ordering == 'featured':
            queryset = queryset.order_by('-is_featured', 'order', '-created_at')
        else:  # default: order
            queryset = queryset.order_by('order', '-is_featured', '-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories for filter
        context['categories'] = GalleryCategory.objects.filter(is_active=True).order_by('order', 'name')
        
        # Get featured images
        context['featured_images'] = GalleryImage.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category', 'location')[:6]
        
        # Statistics
        context['total_images'] = GalleryImage.objects.filter(is_active=True).count()
        
        # Current filters
        context['current_category'] = self.request.GET.get('category', '')
        context['current_location'] = self.request.GET.get('location', '')
        context['current_search'] = self.request.GET.get('search', '')
        context['current_ordering'] = self.request.GET.get('ordering', 'order')
        
        return context


class GalleryDetailView(DetailView):
    """Gallery image detail page (for lightbox)"""
    model = GalleryImage
    template_name = 'gallery/detail.html'
    context_object_name = 'image'
    pk_url_kwarg = 'pk'
    
    def get_queryset(self):
        return GalleryImage.objects.filter(is_active=True).select_related(
            'category', 'location'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.object
        
        # Get related images (same category)
        if image.category:
            context['related_images'] = GalleryImage.objects.filter(
                category=image.category,
                is_active=True
            ).exclude(id=image.id).select_related('category', 'location')[:12]
        
        # Get all images for lightbox navigation
        all_images = GalleryImage.objects.filter(is_active=True).order_by('order', '-is_featured', '-created_at')
        image_list = list(all_images)
        try:
            current_index = image_list.index(image)
            context['prev_image'] = image_list[current_index - 1] if current_index > 0 else None
            context['next_image'] = image_list[current_index + 1] if current_index < len(image_list) - 1 else None
        except ValueError:
            context['prev_image'] = None
            context['next_image'] = None
        
        return context

