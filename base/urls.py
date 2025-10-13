from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

from frontend.sitemap import StaticViewSitemap, CategorySitemap, ProductSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "categories": CategorySitemap,
    "products": ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace="frontend")),
    path('store', include('store.urls', namespace="store")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('robots.txt', robots_txt),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)