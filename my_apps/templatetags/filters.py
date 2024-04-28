from django import template

register = template.Library()


@register.filter
def get_count_value(d: dict, k):
    return d.get(k)['count']


@register.filter
def get_events_values(d: dict, k):
    return d.get(k)['event']