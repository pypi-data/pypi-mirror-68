from django import template

register = template.Library()


@register.filter
def batch(iterable, size=3):
    count = len(iterable)
    for ndx in range(0, count, size):
        elements = iterable[ndx : min(ndx + size, count)]
        yield elements + [None] * (size - len(elements))
