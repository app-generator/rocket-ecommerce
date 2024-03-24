from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.common.models import Product

class StaticSitemap(Sitemap):
    priority = 0.9

    def items(self):
        return ['home_page', 'discounts', 'search_page', 'privacy_policy', 'terms_condition', 'help', 'category_list']
    
    def location(self, item):
        return reverse(item)


class DynamicSitemap(Sitemap):
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created_at