import random
from django import template


register = template.Library()


@register.simple_tag
def bust_cache(value):
    chunk = str(random.randint(10000, 99999))
    if '?' not in value:
        return value + '?' + chunk
    if value[-1] == '?' or value[-1] == '&':
        return value + chunk
    return value + '&' + chunk
