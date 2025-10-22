from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .cart import Cart

@receiver(user_logged_in)
def load_cart_on_login(sender, user, request, **kwargs):
    cart = Cart(request)
    cart.sync_to_session()
