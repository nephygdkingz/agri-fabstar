from django.urls import path

from . import views

app_name = "frontend"

urlpatterns = [
    path('', views.home_view, name="home"),
    path("services/", views.services, name="services"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("agricultural-products/", views.agricultural_products_view, name="agricultural_products"),
    path("order/products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),

    path("robots.txt", views.robots_txt, name="robots_txt"),
]
