from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url or 'account:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    context = {
        'next': next_url,
        "meta_title": "Login - Fabstar Limited",
        "meta_description": "Access your Fabstar Limited account to manage orders, track deliveries, and explore exclusive offers.",
        "no_index": True,  # 👈 Prevents indexing
    }
    return render(request, 'account/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("frontend:login")


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_view(request):
    user = request.user

    context = {
        "meta_title": "My Dashboard – Fabstar Limited",
        "meta_description": "Access your account dashboard to view orders, update details, and manage your shopping experience with Fabstar Limited.",
        "no_index": True,  # Prevent search engine indexing
        "user": user,
    }

    return render(request, "account/dashboard.html", context)

