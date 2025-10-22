from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .cart import Cart
from store.models import Product

@require_POST
def cart_add_ajax(request):
    slug = request.POST.get('slug')
    quantity = request.POST.get('quantity', 1)

    print(f'product slug is {slug}')
    print(f'product quantity is {quantity}')

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
