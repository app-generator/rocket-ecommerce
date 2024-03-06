from django import template

register = template.Library()


@register.filter(name="get_total")
def get_total(carts, shipping=0):
    total = 0
    for cart in carts:
        total += cart.total_price
    

    return float(shipping) + float(total)