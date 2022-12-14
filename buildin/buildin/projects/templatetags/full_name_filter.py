from django import template

from buildin.core.service.account_service import get_user_full_name

register = template.Library()


@register.filter
def user_full_name_filter(user):
    if user != None:
        user_full_name = get_user_full_name(user)
        return user_full_name
