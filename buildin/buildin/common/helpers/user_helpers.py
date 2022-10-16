from buildin.accounts.models import Profile


def get_profile_of_current_user(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        return profile
    except:
        return None


def get_full_of_logged_user(request):
    try:
        profile = get_profile_of_current_user(request)
        return profile.full_name
    except:
        return request.user
