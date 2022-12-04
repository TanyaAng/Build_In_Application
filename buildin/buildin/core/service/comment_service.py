from django.core.exceptions import PermissionDenied

from buildin.core.repository.account_repository import get_request_user
from buildin.core.repository.common_repository import get_owner_of_comment


def can_user_update_comment(request, comment):
    user = get_request_user(request)
    comment_owner = get_owner_of_comment(comment)
    if not user == comment_owner:
        return False
    return True


def can_user_delete_comment(request, comment):
    user = get_request_user(request)
    comment_owner = get_owner_of_comment(comment)
    if not user.is_superuser and not user == comment_owner:
        return False
    return True


def handle_user_perm_to_update_comment(request, comment):
    if not can_user_update_comment(request, comment):
        raise PermissionDenied


def handle_user_perm_to_delete_comment(request, comment):
    if not can_user_delete_comment(request, comment):
        raise PermissionDenied
