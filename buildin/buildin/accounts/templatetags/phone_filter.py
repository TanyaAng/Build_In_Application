from django import template

register = template.Library()


@register.filter
def phone_separator(phone):
    phone_str = str(phone)
    new_value = phone_str.replace(', press ', ' ')
    return new_value
