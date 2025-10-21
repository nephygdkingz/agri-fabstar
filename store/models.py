import uuid
import secrets
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True,null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            count = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:category_detail", kwargs={"slug": self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    # image = models.ImageField(upload_to="products/")
    short_description = models.TextField(max_length=300)
    long_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        while Product.objects.filter(slug=slug).exists():
            unique_part = f"{uuid.uuid4().hex[:4]}-{secrets.token_hex(2)}"
            slug = f"{unique_part}-{base_slug}"
        return slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    @property
    def sale_percent(self):
        if self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return round(discount, 1)  # Rounded to 1 decimal
        return 0

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"slug": self.slug})
    

class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    # image = CloudinaryField('image', null=True, default=None, blank=True)
    image = models.ImageField(upload_to='product_image/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"Media for {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Check if any media for this product is already featured
        existing_featured = ProductMedia.objects.filter(product=self.product, is_featured=True)

        # If none is featured and this one isn't explicitly marked, auto-feature it
        if not existing_featured.exists() and not self.is_featured:
            self.is_featured = True

        # If this one is featured, unset others
        if self.is_featured:
            ProductMedia.objects.filter(product=self.product, is_featured=True).exclude(pk=self.pk).update(is_featured=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if this was the featured image
        was_featured = self.is_featured
        product = self.product
        super().delete(*args, **kwargs)

        # If it was featured, promote another media
        if was_featured:
            next_media = ProductMedia.objects.filter(product=product).first()
            if next_media:
                next_media.is_featured = True
                next_media.save()
