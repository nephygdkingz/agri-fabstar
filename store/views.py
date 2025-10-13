from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Category, Product


def category_detail_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.all()

    context = {
        "meta_title": f"{category.name} Products | Fabstar Limited Nigeria",
        "meta_description": f"Explore premium {category.name.lower()} products available across Nigeria by Fabstar Limited.",
        # "og_image": request.build_absolute_uri("/static/images/og-default.jpg"),
        "breadcrumbs": [
            {"title": "Home", "url": reverse("frontend:home")},
            {"title": category.name, "url": None},
        ],
        "category": category,
        "products": products,
    }
    return render(request, "store/category_detail.html", context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        "meta_title": f"{product.name} | Fabstar Limited Nigeria",
        "meta_description": product.short_description,
        "og_image": request.build_absolute_uri(product.image.url if product.image else "/static/images/og-default.jpg"),
        "breadcrumbs": [
            {"title": "Home", "url": reverse("frontend:home")},
            {"title": product.category.name, "url": product.category.get_absolute_url()},
            {"title": product.name, "url": None},
        ],
        "product": product,
    }
    return render(request, "store/product_detail.html", context)
