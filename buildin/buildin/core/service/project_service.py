from django.core.exceptions import PermissionDenied

from buildin.core.repository.account_repository import get_request_user
from buildin.core.repository.project_repository import get_project_participants, get_project_owner


def can_user_get_project(request, project):
    participants = get_project_participants(project)
    user = get_request_user(request)
    project_owner = get_project_owner(project)
    if not user.is_superuser and not user == project_owner and user not in participants:
        return False
    return True


def can_user_update_project(request, project):
    user = get_request_user(request)
    project_owner = get_project_owner(project)
    if not user.is_superuser and not user == project_owner:
        return False
    return True


def can_user_delete_project(request, project):
    user = get_request_user(request)
    project_owner = get_project_owner(project)
    if not user.is_superuser and not user == project_owner:
        return False
    return True


def handle_user_perm_to_get_project(request, project):
    if not can_user_get_project(request, project):
        raise PermissionDenied


def handle_user_perm_to_update_project(request, project):
    if not can_user_update_project(request, project):
        raise PermissionDenied


def handle_user_perm_to_delete_project(request, project):
    if not can_user_delete_project(request, project):
        raise PermissionDenied
