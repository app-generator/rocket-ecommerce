from django import template
from apps.common.models import Cart

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_count(context):
    request = context['request']
    cart_count = Cart.objects.filter(user=request.user).count()
    return cart_count