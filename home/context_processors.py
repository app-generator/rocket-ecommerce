from apps.common.models import Tag, Product, Settings


def product_context(request):

    return {
        'tags': Tag.objects.filter(product__in=Product.objects.all()).distinct(),
        'site_name': Settings.objects.filter(type='site_name').first().value if Settings.objects.filter(type='site_name').exists() else 'Rocket eCommerce',
        'copyright': Settings.objects.filter(type='copyright').first().value if Settings.objects.filter(type='copyright').exists() else 'Appseed',
        'hero_video': Settings.objects.filter(type='hero_video').first().file if Settings.objects.filter(type='hero_video').exists() else None,
        'social_twitter': Settings.objects.filter(type='social_twitter').first().value if Settings.objects.filter(type='social_twitter').exists() else '',
        'social_facebook': Settings.objects.filter(type='social_facebook').first().value if Settings.objects.filter(type='social_facebook').exists() else '',
        'social_github': Settings.objects.filter(type='social_github').first().value if Settings.objects.filter(type='social_github').exists() else '',
        'social_instagram': Settings.objects.filter(type='social_instagram').first().value if Settings.objects.filter(type='social_instagram').exists() else '',
    }