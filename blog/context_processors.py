from .views import get_categories_and_tags

def categories_processor(request):
    categories, _ = get_categories_and_tags()
    return {
        'categories': categories
    }
