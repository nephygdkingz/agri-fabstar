import random
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from datetime import timedelta

from store.models import Product

class Order(models.Model):
    STATUS = (
        ('Pending, awaiting payment', 'Pending, awaiting payment'),
        ('Delivery in Progress', 'Delivery in Progress'),
        ('Delivered', 'Delivered'),
    )
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='order_user' , null=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    order_key = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=150, choices=STATUS, default='Pending, awaiting payment')
    shipping_price = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    # delivery_date = models.DateField(null=True, blank=True)
    # delivery_address = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def get_final_balance(self):
        return self.total - self.paid
    
    def __str__(self):
        return str(self.created)
    

def order_key_post_save(sender, instance, created,*args, **kwargs):
    if created:
        ref = random.randint(00000000, 99999999)
        ref_final = str(int(ref) + instance.id)
        instance.order_key = f'FB-ST-AR{ref_final}K3Y'
        instance.save()

post_save.connect(order_key_post_save, sender=Order)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_item_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return str(self.id)