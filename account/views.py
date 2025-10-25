from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

from store.forms import AddProductForm, MediaFormSet, EditMediaFormSet
from store.models import Product
from order.models import Order
from frontend.turnstile import verify_turnstile

# Only allow staff or superusers
def admin_required(user):
    return user.is_staff or user.is_superuser

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        # verify turnstile
        # if not verify_turnstile(request):
        #     messages.error(request, "Please verify you are not a bot.")
        #     return redirect("account:login")
        
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
        "turnstile": True,
    }
    return render(request, 'account/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("account:login")


@login_required
@user_passes_test(admin_required)
def dashboard_view(request):
    user = request.user

    # Query all products and orders
    products = Product.objects.all().order_by("-created_at")  
    orders = Order.objects.all().order_by("-created")

    # --- PAGINATION ---
    product_paginator = Paginator(products, 10)  # 10 products per page
    order_paginator = Paginator(orders, 10)      # 10 orders per page

    # Get page numbers from query params (?product_page=2&order_page=3)
    product_page_number = request.GET.get("product_page")
    order_page_number = request.GET.get("order_page")

    # Get the correct page objects
    product_page = product_paginator.get_page(product_page_number)
    order_page = order_paginator.get_page(order_page_number)

    context = {
        "meta_title": "My Dashboard - Fabstar Limited",
        "meta_description": "Access your account dashboard to view orders, update details, and manage your shopping experience with Fabstar Limited.",
        "no_index": True,
        "user": user,
        "product_page": product_page,
        "order_page": order_page,
    }

    return render(request, "account/main_dashboard.html", context)

@login_required
@user_passes_test(admin_required)
def add_product_view(request):
    form = AddProductForm(request.POST or None)
    media_form = MediaFormSet(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid() and media_form.is_valid():
            product = form.save()

            # Save related media items
            media_instances = media_form.save(commit=False)
            for media in media_instances:
                media.product = product
                media.save()

            # Optionally handle deletions in formset
            for deleted_media in media_form.deleted_objects:
                deleted_media.delete()

            messages.success(request, "Product added successfully.")
            return redirect("account:add_product")  

    context = {
        "meta_title": "Add New Product - Fabstar Limited Admin",
        "meta_description": "Add new agricultural, livestock, or gas products to the Fabstar Limited online store.",
        "no_index": True,
        "form": form,
        "media_form": media_form,
        "title": "Add",
    }
    return render(request, "account/admin/add_product.html", context)


@login_required
@user_passes_test(admin_required)
def edit_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    form = AddProductForm(request.POST or None, instance=product)
    media_form = EditMediaFormSet(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST":
        if form.is_valid() and media_form.is_valid():
            form.save()          # ✅ Updates the existing product
            media_form.save()    # ✅ Handles add, update, delete for related media automatically

            messages.success(request, "Product updated successfully.")
            return redirect("account:dashboard")
            # Or redirect back to edit page if you prefer:
            # return redirect("account:edit_product", pk=product.pk)

    context = {
        "meta_title": f"Edit Product - {product.name} | Fabstar Limited Admin",
        "meta_description": "Edit existing agricultural, livestock, or gas products in the Fabstar Limited online store.",
        "no_index": True,
        "form": form,
        "media_form": media_form,
        "title": "Edit",
        "product": product,
    }
    return render(request, "account/admin/add_product.html", context)


@login_required
@user_passes_test(admin_required)
def delete_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        # Delete related ProductMedia first (if not set to cascade)
        product.media.all().delete()
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully.")
        return redirect("account:dashboard")

    context = {
        "meta_title": f"Delete Product - {product.name} | Fabstar Limited Admin",
        "meta_description": "Confirm deletion of a product from the Fabstar Limited online store.",
        "no_index": True,
        "product": product,
        "title": "Delete",
    }
    return render(request, "account/admin/delete_product.html", context)


