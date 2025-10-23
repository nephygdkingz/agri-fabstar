def default_meta(request):
    base_url = request.build_absolute_uri('/')[:-1]  # e.g. "https://www.fabstarlimited.com"

    return {
        "site_name": "Fabstar Limited",
        "default_meta_title": "Fabstar Limited | Agricultural, Livestock & Gas Products in Nigeria",
        "default_meta_description": (
            "Fabstar Limited is Nigeria's leading supplier of agricultural products, "
            "livestock, poultry, and gas equipment. Trusted quality nationwide."
        ),
        "default_meta_keywords": "fabstar, agriculture nigeria, livestock, poultry, farm produce, gas plant, agrotech",
        "default_og_image": f"{base_url}/static/frontend/images/heroes/hero-5.jpg",
        "default_logo_url": f"{base_url}/static/frontend/images/logo.png",
        "canonical_url": request.build_absolute_uri(request.path),
    }


from django.conf import settings

def turnstile_keys(request):
    """Add Cloudflare Turnstile site key to all templates."""
    return {
        "TURNSTILE_SITE_KEY": getattr(settings, "TURNSTILE_SITE_KEY", "")
    }
