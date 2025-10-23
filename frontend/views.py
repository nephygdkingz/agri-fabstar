from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Q

from .decorators import redirect_authenticated
from store.models import Product, Category
from cart.email_utils import send_contact_form_notification
from frontend.turnstile import verify_turnstile

@redirect_authenticated('account:dashboard')
def home_view(request):
    featured_products = Product.objects.filter(is_available=True,is_featured=True)
    context = {
        "featured_products": featured_products,
        "meta_title": "Fabstar Limited | Agricultural, Livestock & Gas Solutions in Nigeria",
        "meta_description": (
            "Welcome to Fabstar Limited — your one-stop Nigerian marketplace for high-quality "
            "agricultural produce, livestock, poultry, and gas plant equipment."
        ),
        "meta_keywords": "Fabstar Limited, agriculture nigeria, livestock, gas plant, farm produce, poultry, agromarket",
        "breadcrumbs": [
            {"title": "Home", "url": reverse("frontend:home")},
        ],
    }
    return render(request, 'frontend/index.html', context)


@redirect_authenticated('account:dashboard')
def about_view(request):
    context = {
        "meta_title": "About Fabstar Limited | Agricultural, Livestock & Gas Experts in Nigeria",
        "meta_description": (
            "Learn about Fabstar Limited — a trusted Nigerian company providing "
            "agricultural products, livestock, and gas solutions with a focus on sustainability and innovation."
        ),
        "og_image": request.build_absolute_uri("/static/images/og-about.jpg"),
        "breadcrumbs": [
            {"title": "Home", "url": reverse("frontend:home")},
            {"title": "About Us", "url": None},
        ],
    }
    return render(request, "frontend/about2.html", context)


@redirect_authenticated('account:dashboard')
def services(request):
    meta_title = "Our Services - Fabstar Limited"
    meta_description = (
        "Fabstar Limited offers premium agricultural products, healthy livestock, "
        "and safe gas retail services across Nigeria. Supplying farms, homes, and businesses."
    )
    context = {
        "meta_title": meta_title,
        "meta_description": meta_description,
    }

    return render(request, "frontend/services.html", context)


@redirect_authenticated('account:dashboard')
def contact_view(request):
    if request.method == "POST":
        # verify turnstile
        if not verify_turnstile(request):
            messages.error(request, "Please verify you are not a bot.")
            return redirect("frontend:contact")
        
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        phone = request.POST.get("phone")

        try:
            # Send internal notification to Fabstar
            send_contact_form_notification(name, email, subject, message, phone)

            messages.success(request, "Your message has been sent successfully. Our team will get back to you soon.")
            
            return redirect("frontend:contact")
        except Exception as e:
            messages.error(request, "An error occurred while sending your message. Please try again.")

    context = {
        "meta_title": "Contact Fabstar Limited | Agricultural, Livestock & Gas Solutions in Nigeria",
        "meta_description": (
            "Get in touch with Fabstar Limited for inquiries about our agricultural products, "
            "livestock services, and gas plant solutions in Nigeria."
        ),
        "og_image": request.build_absolute_uri("/static/images/og-contact.jpg"),
        "breadcrumbs": [
            {"title": "Home", "url": reverse("frontend:home")},
            {"title": "Contact Us", "url": None},
        ],
        "turnstile": True,
    }
    return render(request, "frontend/contact.html", context)

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /accounts/",
        "Allow: /",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@redirect_authenticated('account:dashboard')
def product_list(request):
    # products = Product.objects.filter(is_available=True).select_related("category")
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    meta_title = "Order Products - Fabstar Limited"
    meta_description = (
        "Order high-quality agricultural products, livestock, and gas supplies from Fabstar Limited. "
        "Reliable and affordable products across Nigeria."
    )
    context = {
        "products": products,
        "categories": categories,
        "meta_title": meta_title,
        "meta_description": meta_description,
    }
    return render(request, "frontend/product_list.html", context)


@redirect_authenticated('account:dashboard')
def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug, is_available=True)
    images = product.media.all() 

    # Get related products from the same category (excluding current one)
    related_products = (
        Product.objects.filter(
            Q(category=product.category) & ~Q(id=product.id),
            is_available=True
        )
        .select_related("category")
        .order_by("?")[:4]  # random 4 items
    )

    meta_title = f"{product.name} - Fabstar Limited"
    meta_description = (
        f"Buy {product.name} from Fabstar Limited. {product.short_description[:150]} "
        "Available for customers across Nigeria."
    )

    context = {
        "product": product,
        'images': images,
        "related_products": related_products,
        "meta_title": meta_title,
        "meta_description": meta_description,
    }

    return render(request, "frontend/product_detail.html", context)
