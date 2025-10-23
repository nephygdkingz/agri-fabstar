from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CheckoutForm
from store.models import Product
from order.models import Order, OrderItem
from .email_utils import send_order_confirmation_email, send_internal_order_notification

def cart_detail(request):
    cart = Cart(request)
    cart_items = list(cart)  # __iter__ gives you all cart items
    cart_total = cart.get_total_price()
    
    return render(request, 'cart/cart_summary.html', {
        'cart_items': cart_items,
        'cart_total': f"{cart_total:.2f}",
        'shipping': cart.get_shipping_cost(),
        'final_total': cart.get_final_total(),
        "meta_title": "Your Shopping Cart - Fabstar Limited",
        "meta_description": "Review items in your cart and proceed to checkout. Secure and fast ordering from Fabstar Limited.",
        "no_index": True,
    })


@require_POST
def cart_add_ajax(request):
    slug = request.POST.get('slug')
    quantity = request.POST.get('quantity', 1)

    if not slug:
        return JsonResponse({'success': False, 'error': 'No product slug provided'})
    
    try:
        product = Product.objects.get(slug=slug)
        quantity = int(quantity)
        cart = Cart(request)
        cart.add(product=product, quantity=quantity)
        return JsonResponse({
            'success': True,
            'cartCount': len(cart),
            'message': f'Added {product.name} (x{quantity}) to cart.'
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
@require_POST
def cart_update_ajax(request):
    slug = request.POST.get('slug')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, slug=slug)

    cart = Cart(request)
    cart.add(product, quantity=quantity, override_quantity=True)

    item_total = 0
    for item in cart:
        if product.id == item['product_obj'].id:
            item_total = item['total_price']
            break

    return JsonResponse({
        'success': True,
        'itemTotal': f'{item_total:.2f}',
        'cartTotal': f'{cart.get_total_price():.2f}',
        'finalTotal': f'{cart.get_final_total():.2f}',
        'cartCount': len(cart),
    })

@require_POST
def cart_remove_ajax(request):
    slug = request.POST.get('slug')
    product = get_object_or_404(Product, slug=slug)

    cart = Cart(request)
    cart.remove(product)

    return JsonResponse({
        'success': True,
        'cartTotal': f'{cart.get_total_price():.2f}',
        'finalTotal': f'{cart.get_final_total():.2f}',
        'cartCount': len(cart),
        
    })


def checkout_view(request):
    cart = Cart(request)
    cart_items = list(cart)
    cart_total = cart.get_total_price()
    shipping_cost = cart.get_shipping_cost()
    final_total = cart.get_final_total()

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            order = Order.objects.create(
                full_name=f"{data['first_name']} {data['last_name']}",
                email=data['email'],
                phone=data['phone'],
                country=data['country'],
                city=data['city'],
                address=data['address'],
                total=cart_total,
                shipping_price=shipping_cost,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product_obj'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            
            # Send customer confirmation email
            send_order_confirmation_email(order)

            # Send internal Fabstar notification
            send_internal_order_notification(order)

            # Optional: clear cart
            cart.clear()

            # Redirect to success page with order ID
            return redirect("cart:order_success", order_id=order.pk)
    else:
        form = CheckoutForm()

    context = {
        "form": form,
        "cart_items": cart_items,
        "cart_total": f"{cart_total:.2f}",
        "shipping": shipping_cost,
        "final_total": final_total,
        "meta_title": "Checkout - Fabstar Limited",
        "meta_description": "Complete your purchase securely with Fabstar Limited.",
        "no_index": True,
    }

    return render(request, "cart/checkout.html", context)


def order_success(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_items = order.items.all()
    context = {
        "meta_title": "Order Successful – Fabstar Limited",
        "meta_description": "Thank you for shopping with Fabstar Limited. Your order has been received successfully. We’ll contact you soon for delivery confirmation.",
        "no_index": True,  # 👈 Prevents Google from indexing this page
        "order":order,
        "order_items":order_items,
    }
    return render(request, "cart/order_success.html", context)