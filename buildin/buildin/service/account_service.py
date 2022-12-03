from django.core.exceptions import PermissionDenied

from buildin.repository.account_repository import get_profile_of_current_user


def get_user_full_name(request):
    try:
        profile = get_profile_of_current_user(request)
        if profile:
            return profile.full_name
    except Exception as ex:
        print(ex)
        return request.user


def handle_user_permissions_to_object(request, object, participants):
    if request.user.is_superuser:
        return True
    if request.user == object.owner or request.user in participants:
        return True
    else:
        raise PermissionDenied
