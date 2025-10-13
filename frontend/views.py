from django.shortcuts import render

def home_view(request):
    context = {
        "meta_title": "Fabstar Limited | Agricultural, Livestock & Gas Solutions in Nigeria",
        "meta_description": (
            "Welcome to Fabstar Limited — your one-stop Nigerian marketplace for high-quality "
            "agricultural produce, livestock, poultry, and gas plant equipment."
        ),
        "meta_keywords": "Fabstar Limited, agriculture nigeria, livestock, gas plant, farm produce, poultry, agromarket",
    }
    return render(request, 'frontend/index.html', context)
