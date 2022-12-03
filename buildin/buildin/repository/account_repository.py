from buildin.accounts.models import Profile


def get_request_user(request):
    return request.user


def get_request_user_id(request):
    return request.user.pk


def find_profile_by_pk(pk):
    return Profile.objects.filter(pk=pk)


def get_profile_by_pk(pk):
    profile = Profile.objects.filter(pk=pk)
    return profile.get()


def get_profile_of_current_user(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return profile


def get_user_by_profile(profile):
    user = profile.user_id
    return user


