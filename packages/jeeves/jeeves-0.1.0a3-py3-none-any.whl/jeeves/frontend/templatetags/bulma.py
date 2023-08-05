from django import template

register = template.Library()


@register.filter
def to_bulma(value):
    """Transform messages tags to bulma classes"""
    mapping = {
        "debug": "is-primary",
        "info": "is-info",
        "success": "is-success",
        "warning": "is-warning",
        "error": "is-danger",
    }
    return mapping[value]
