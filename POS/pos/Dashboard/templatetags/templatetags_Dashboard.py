from django import template

register = template.Library()


@register.filter
def lookup(values, key):
    return values[key]


@register.filter
def multiply(a, b):
    return float(a) * float(b)
