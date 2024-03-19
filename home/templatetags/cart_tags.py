from django import template
from apps.common.models import Cart

register = template.Library()

@register.filter(name="cart_count")
def cart_count(user):
    if user.is_authenticated:
        cart_count = Cart.objects.filter(user=user, is_ordered=False).count()
        return cart_count
    else:
        return 0