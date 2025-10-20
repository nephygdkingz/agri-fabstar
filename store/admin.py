from django.contrib import admin

from .models import Category, Product, ProductMedia

admin.site.register(Category)

class ProductMediaInline(admin.TabularInline):  
    model = ProductMedia
    extra = 1
    fields = ['image', 'alt_text', 'is_featured']
    readonly_fields = []

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available', 'category', 'slug']
    inlines = [ProductMediaInline]

# admin.site.register(Product)
