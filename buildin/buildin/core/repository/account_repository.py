from buildin.accounts.models import Profile, BuildInUser


def get_request_user(request):
    return request.user


def get_request_user_id(request):
    return request.user.pk


def get_user_id_by_profile(profile):
    user_id = profile.user_id
    return user_id


def get_users_by_profiles(profiles):
    users = BuildInUser.objects.filter(pk__in=profiles)
    return users


def find_profile_by_pk(pk):
    return Profile.objects.filter(pk=pk)


def get_profile_by_pk(pk):
    profile = Profile.objects.filter(pk=pk)
    return profile.get()


def get_profile_full_name(profile):
    return profile.full_name


def get_profile_of_request_user(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return profile


def get_profile_of_user(user):
    profile = Profile.objects.get(user_id=user.pk)
    return profile


def get_profiles_of_participants(participants):
    profiles = Profile.objects.filter(user__in=participants)
    return profiles
