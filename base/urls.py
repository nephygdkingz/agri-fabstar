from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from frontend.sitemap import FabstarSitemap
from django.http import HttpResponse

sitemaps = {
    'static': FabstarSitemap,
}

def robots_txt(request):
    content = (
        "User-Agent: *\n"
        "Disallow:\n"
        "Sitemap: https://www.fabstarlimited.com/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace="frontend")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)