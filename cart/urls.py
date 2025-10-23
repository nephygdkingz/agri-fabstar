from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add-ajax/', views.cart_add_ajax, name='cart_add_ajax'),
    path('update-ajax/', views.cart_update_ajax, name='cart_update_ajax'),
    path('remove-ajax/', views.cart_remove_ajax, name='cart_remove_ajax'),

    path('checkout/', views.checkout_view, name='checkout'),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    # path('checkout/process/', views.process_checkout, name='process_checkout'),
]