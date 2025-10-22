from decimal import Decimal
from django.conf import settings
from .models import Product, CartItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_slug = product.slug  # use slug as key

        # Session cart update
        if product_slug not in self.cart:
            self.cart[product_slug] = {
                'quantity': 0,
                'price': str(product.price),
                'name': product.name,
                'slug': product.slug,
            }

        if override_quantity:
            self.cart[product_slug]['quantity'] = quantity
        else:
            self.cart[product_slug]['quantity'] += quantity

        self.save()

        # DB cart update for logged-in users
        if self.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(user=self.user, product=product)
            if override_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_slug = product.slug
        if product_slug in self.cart:
            del self.cart[product_slug]
            self.save()

        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user, product=product).delete()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user).delete()

    def __iter__(self):
        product_slugs = self.cart.keys()
        products = Product.objects.filter(slug__in=product_slugs)
        for product in products:
            item = self.cart[product.slug].copy()  # copy dict to avoid mutation issues
            item['product_obj'] = product
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_shipping_cost(self):
        return Decimal("2500.00")  # or logic to calculate dynamically

    def get_final_total(self):
        return self.get_total_price() + self.get_shipping_cost()

    def sync_to_session(self):
        if self.user.is_authenticated:
            self.cart = {}
            for item in CartItem.objects.filter(user=self.user):
                self.cart[item.product.slug] = {
                    'quantity': item.quantity,
                    'price': str(item.product.price),
                    'name': item.product.name,
                    'slug': item.product.slug,
                }
            self.save()
