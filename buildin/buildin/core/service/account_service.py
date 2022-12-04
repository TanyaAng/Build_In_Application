from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist

from buildin.accounts.models import Profile
from buildin.core.repository.account_repository import get_profile_of_current_user, get_request_user_id, \
    get_user_id_by_profile, get_request_user


def get_user_full_name(request):
    try:
        profile = get_profile_of_current_user(request)
        if profile:
            full_name = profile.full_name
            return full_name
    except ObjectDoesNotExist:
        username = get_request_user(request)
        return username


def if_request_user_is_owner_of_profile(request, profile):
    request_user_id = get_request_user_id(request)
    profile_user_id = get_user_id_by_profile(profile)
    if not request_user_id == profile_user_id:
        return False
    return True


def login_after_registration(request, user):
    login(request, user)


def check_if_user_has_profile(user):
    if Profile.objects.filter(user_id=user.pk):
        return True
    return False
