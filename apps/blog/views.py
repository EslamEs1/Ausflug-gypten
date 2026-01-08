"""
Blog views
"""

from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import BlogPost, BlogCategory
from apps.core.models import PageHero


class BlogListView(ListView):
    """List all blog posts"""
    model = BlogPost
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True).select_related('category', 'author')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(title_en__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(excerpt_en__icontains=search) |
                Q(content__icontains=search)
            )
        
        return queryset.order_by('-published_at', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(is_active=True).order_by('name')
        
        # Get featured post (first published post)
        context['featured_post'] = BlogPost.objects.filter(
            is_published=True
        ).select_related('category', 'author').first()
        
        # Current filter
        context['current_category'] = self.request.GET.get('category', '')
        context['current_search'] = self.request.GET.get('search', '')
        
        # Page Hero
        try:
            context['page_hero'] = PageHero.objects.filter(page='blog', is_active=True).prefetch_related('badges').first()
        except PageHero.DoesNotExist:
            context['page_hero'] = None
        
        return context


class BlogDetailView(DetailView):
    """Blog post detail"""
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).select_related('category', 'author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # Related posts (same category)
        if post.category:
            context['related_posts'] = BlogPost.objects.filter(
                is_published=True,
                category=post.category
            ).exclude(id=post.id).select_related('category', 'author')[:3]
        else:
            context['related_posts'] = BlogPost.objects.filter(
                is_published=True
            ).exclude(id=post.id).select_related('category', 'author')[:3]
        
        # Get all categories for sidebar
        context['categories'] = BlogCategory.objects.filter(is_active=True).order_by('name')
        
        # Get recent posts for sidebar
        context['recent_posts'] = BlogPost.objects.filter(
            is_published=True
        ).exclude(id=post.id).select_related('category', 'author')[:5]
        
        return context

