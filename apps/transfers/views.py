"""
Views for Transfers app
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Transfer, TransferType, VehicleType


class TransferListView(ListView):
    """List all transfers with filtering"""
    model = Transfer
    template_name = 'transfer/index.html'
    context_object_name = 'transfers'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Transfer.objects.filter(is_active=True).select_related(
            'transfer_type', 'vehicle_type', 'from_location', 'to_location'
        )
        
        # Filter by transfer type
        type_slug = self.request.GET.get('type')
        if type_slug:
            queryset = queryset.filter(transfer_type__slug=type_slug)
        
        # Filter by vehicle type
        vehicle_slug = self.request.GET.get('vehicle')
        if vehicle_slug:
            queryset = queryset.filter(vehicle_type__slug=vehicle_slug)
        
        # Filter by from location
        from_location = self.request.GET.get('from')
        if from_location:
            queryset = queryset.filter(from_location__slug=from_location)
        
        # Filter by to location
        to_location = self.request.GET.get('to')
        if to_location:
            queryset = queryset.filter(to_location__slug=to_location)
        
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
            queryset = queryset.order_by('base_price')
        elif ordering == 'price_high':
            queryset = queryset.order_by('-base_price')
        elif ordering == 'popular':
            queryset = queryset.order_by('-is_popular', '-is_featured', 'title')
        else:  # featured/default
            queryset = queryset.order_by('-is_featured', '-is_popular', 'title')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all transfer types for filter
        context['transfer_types'] = TransferType.objects.filter(is_active=True).order_by('order', 'name')
        
        # Get all vehicle types for filter
        context['vehicle_types'] = VehicleType.objects.filter(is_active=True).order_by('order', 'capacity')
        
        # Get featured transfers
        context['featured_transfers'] = Transfer.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('transfer_type', 'vehicle_type')[:6]
        
        # Statistics
        context['total_transfers'] = Transfer.objects.filter(is_active=True).count()
        
        # Current filters
        context['current_type'] = self.request.GET.get('type', '')
        context['current_vehicle'] = self.request.GET.get('vehicle', '')
        context['current_from'] = self.request.GET.get('from', '')
        context['current_to'] = self.request.GET.get('to', '')
        context['current_search'] = self.request.GET.get('search', '')
        context['current_ordering'] = self.request.GET.get('ordering', 'featured')
        
        return context


class TransferDetailView(DetailView):
    """Transfer detail page"""
    model = Transfer
    template_name = 'transfer/detail.html'
    context_object_name = 'transfer'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Transfer.objects.filter(is_active=True).select_related(
            'transfer_type', 'vehicle_type', 'from_location', 'to_location'
        ).prefetch_related(
            'images',
            'inclusions',
            'important_info',
            'routes'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transfer = self.object
        
        # Get related transfers (same type)
        context['related_transfers'] = Transfer.objects.filter(
            transfer_type=transfer.transfer_type,
            is_active=True
        ).exclude(id=transfer.id).select_related('transfer_type', 'vehicle_type')[:4]
        
        # Get transfers with same vehicle type
        if transfer.vehicle_type:
            context['similar_vehicles'] = Transfer.objects.filter(
                vehicle_type=transfer.vehicle_type,
                is_active=True
            ).exclude(id=transfer.id).select_related('transfer_type', 'vehicle_type')[:3]
        
        # Get average rating (if reviews are implemented)
        context['average_rating'] = 5.0  # Placeholder
        context['total_reviews'] = 0  # Placeholder
        
        return context

