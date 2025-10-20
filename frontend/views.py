from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Q

from store.models import Product

def home_view(request):
    context = {
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

def services():
    pass

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

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Construct email message
        email_subject = f"New Contact Message from {name}"
        email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            email_message = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=email,
                to=["info@fabstarlimited.com"],  # Change to your real contact email
                reply_to=[email],
            )
            email_message.send(fail_silently=False)
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
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
    }
    return render(request, "frontend/contact.html", context)

def agricultural_products_view(request):
    context = {
        "meta_title": "Agricultural Products | Fabstar Limited Nigeria",
        "meta_description": (
            "Shop top-quality Nigerian agricultural products — including seeds, grains, fertilizers, "
            "and farm equipment — supplied by Fabstar Limited."
        ),
        "og_image": request.build_absolute_uri("/static/images/og-agriculture.jpg"),
        "breadcrumbs": [
            {"title": "Home", "url": reverse("frontend:home")},
            {"title": "Agricultural Products", "url": None},
        ],
        # Example placeholder data (you can later replace this with real DB data)
        "products": [
            {
                "name": "Maize Seeds",
                "image": "/static/images/products/maize.jpg",
                "description": "High-yield hybrid maize seeds suitable for Nigerian soil.",
            },
            {
                "name": "Fertilizers",
                "image": "/static/images/products/fertilizer.jpg",
                "description": "Organic and chemical fertilizers for better crop productivity.",
            },
            {
                "name": "Cassava Stems",
                "image": "/static/images/products/cassava.jpg",
                "description": "Disease-resistant cassava varieties ready for planting.",
            },
            {
                "name": "Farm Tools",
                "image": "/static/images/products/tools.jpg",
                "description": "Durable farm tools and equipment for all farming operations.",
            },
        ],
    }
    return render(request, "frontend/agricultural_products.html", context)

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


def product_list(request):
    products = Product.objects.filter(is_available=True).select_related("category")

    meta_title = "Order Products - Fabstar Limited"
    meta_description = (
        "Order high-quality agricultural products, livestock, and gas supplies from Fabstar Limited. "
        "Reliable and affordable products across Nigeria."
    )
    context = {
        "products": products,
        "meta_title": meta_title,
        "meta_description": meta_description,
    }
    return render(request, "frontend/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug, is_available=True)

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
        "related_products": related_products,
        "meta_title": meta_title,
        "meta_description": meta_description,
    }

    return render(request, "frontend/product_detail.html", context)
