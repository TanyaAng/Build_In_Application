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


def handle_user_permissions_to_access_project(request, object, participants):
    if request.user.is_superuser:
        return True
    if request.user == object.owner or request.user in participants:
        return True
    else:
        raise PermissionDenied


def handle_user_CRUD_permissions_to_project(request, object):
    if request.user.is_superuser or request.user == object.owner:
        return True
    else:
        raise PermissionDenied


def handle_user_CRUD_permissions_to_edit_comment(request, comment):
    if request.user.is_superuser or request.user == comment.user:
        return True
    else:
        raise PermissionDenied


def handle_user_CRUD_permissions_to_delete_comment(request, comment):
    if request.user.is_superuser or request.user == comment.user:
        return True
    else:
        raise PermissionDenied
