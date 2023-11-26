from django import template
register = template.Library()

@register.filter(name='mongo_id')
def mongo_id(value):
    return str(value['_id'])