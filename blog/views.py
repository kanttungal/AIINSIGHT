from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from taggit.models import Tag
from .models import Post, Category

def get_categories_and_tags():
    categories = Category.objects.all().prefetch_related('posts')
    # Add post count to each category
    for category in categories:
        category.post_count = category.posts.filter(status='published').count()
    tags = Tag.objects.all()
    return categories, tags

def about(request):
    # Get categories and tags for sidebar
    categories, tags = get_categories_and_tags()
    
    context = {
        'categories': categories,
        'tags': tags,
    }
    
    return render(request, 'blog/about.html', context)

def post_list(request, category_slug=None, tag_slug=None):
    posts = Post.objects.filter(status='published')
    
    category = None
    tag = None
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    
    # Pagination
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get latest 3 posts for featured section
    latest_posts = Post.objects.filter(status='published')[:3]
    
    # Get categories and tags for sidebar
    categories, tags = get_categories_and_tags()
    
    context = {
        'page_obj': page_obj,
        'latest_posts': latest_posts,
        'category': category,
        'tag': tag,
        'categories': categories,
        'tags': tags,
    }
    
    return render(request, 'blog/post_list.html', context)

def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status='published')
    
    # Get related posts by category (excluding current post)
    related_posts = Post.objects.filter(
        category=post.category, 
        status='published'
    ).exclude(id=post.id)[:3]
    
    # Get categories and tags for sidebar
    categories, tags = get_categories_and_tags()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'categories': categories,
        'tags': tags,
    }
    
    return render(request, 'blog/post_detail.html', context)

def post_search(request):
    query = None
    results = []
    
    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            results = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            ).filter(status='published').distinct()
    
    # Get categories for sidebar
    categories, tags = get_categories_and_tags()
    
    context = {
        'query': query,
        'results': results,
        'categories': categories,
        'tags': tags,
    }
    
    return render(request, 'blog/search_results.html', context)
