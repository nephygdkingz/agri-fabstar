from .models import Category

def categories_processor(request):
    """
    Adds all active product categories to the template context.
    """
    categories = Category.objects.filter(is_active=True).order_by("name")
    return {"nav_categories": categories}
