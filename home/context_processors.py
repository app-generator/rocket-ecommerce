from apps.common.models import Tag, Product


def product_context(request):
    return {
        'tags': Tag.objects.filter(product__in=Product.objects.all()).distinct()
    }