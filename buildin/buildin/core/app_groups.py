from django.contrib.auth.models import Group


def set_user_to_regular_user_group(user):
    regular_user_group = Group.objects.get(name='Regular User')
    regular_user_group.user_set.add(user)


def set_user_to_admin_group(user):
    admin_user_group = Group.objects.get(name='Admin')
    admin_user_group.user_set.add(user)
