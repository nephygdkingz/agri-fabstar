from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("category/<slug:slug>/", views.category_detail_view, name="category_detail"),
    path("product/<slug:slug>/", views.product_detail_view, name="product_detail"),
]
