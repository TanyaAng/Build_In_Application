from django import template

register = template.Library()


@register.filter
def has_perm_to_view_logactivity(user):
    if user.has_perm('common.view_logactivity'):
        return True
    return False
