from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    path("admin/add-product/", views.add_product_view, name="add_product"),
    path("admin/edit-product/<pk>/", views.edit_product_view, name="edit_product"),
    path("product/<int:pk>/delete/", views.delete_product_view, name="delete_product"),

]