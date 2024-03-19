from django import template
from apps.common.models import Settings

register = template.Library()

@register.filter(name="get_values")
def get_values(type):
    settings = Settings.objects.filter(type=type)
    if settings.exists():
        return settings.first().value
    else:
        return ''