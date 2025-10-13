from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class FabstarSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # list all named URLs you want indexed
        return ['home']

    def location(self, item):
        # if your urls are under namespace 'frontend'
        return reverse(f'frontend:{item}')
