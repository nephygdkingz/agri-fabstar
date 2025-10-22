from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .cart import Cart
from store.models import Product

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