from django.contrib.auth import views as auth_views
from django.views import generic as generic_views
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import render, redirect


from buildin.repository.account_repository import get_profile_by_pk, get_user_full_name, find_profile_by_pk, \
    get_user_by_found_profile
from buildin.repository.project_repository import get_user_projects_where_user_is_participant_or_owner

from buildin.repository.task_repository import get_user_tasks

from buildin.accounts.forms import UserRegistrationForm, EditProfileForm, CreateProfileForm

UserModel = auth_views.get_user_model()


class UserRegisterView(generic_views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context['profile_form']=ProfileCreateForm
    #     return context

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        # custom logic - login automatically after registration
        user = self.object
        request = self.request
        login(request, user)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


# FBV logout
# def user_logout_view(request):
#     if request.user.is_authenticated:
#         logout(request)
#     return redirect('home page')


class UserLogoutView(auth_views.LogoutView):
    # Logout success url is set in Setting.py
    pass


# class ProfileDetailsView(generic_views.DetailView):
#     model = Profile
#     template_name = 'accounts/profile-details.html'
#     context_object_name = 'profile'

# def dispatch(self, request, *args, **kwargs):
# if self.object is None:
#     return redirect('profile create')
# print(self.object)
# return super().dispatch(request, *args, **kwargs)

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     user = self.object.user_id
#
#     user_projects = BuildInProject.objects.filter(
#         Q(participants__exact=user) |
#         Q(owner_id=user)
#     )
#     user_tasks = ProjectTask.objects.filter(
#         Q(designer__exact=user) | Q(checked_by__exact=user))
#
#     context['user_projects'] = user_projects.distinct()
#     context['user_tasks'] = user_tasks
#     context['user_full_name'] = get_full_name_current_user(self.request)
#     return context



def profile_details(request, pk):
    found_profile = find_profile_by_pk(pk)
    if not found_profile:
        return redirect('profile create')

    profile=found_profile.get()
    user = get_user_by_found_profile(profile)
    user_full_name = get_user_full_name(request)
    user_projects = get_user_projects_where_user_is_participant_or_owner(user)
    user_tasks = get_user_tasks(user)

    context = {
        'profile': profile,
        'user_full_name': user_full_name,
        'user_projects': user_projects.distinct(),
        'user_tasks': user_tasks,
    }
    return render(request, 'accounts/profile-details.html', context)


def profile_create(request):
    if request.method == 'GET':
        form = CreateProfileForm()
    else:
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile details', profile.user_id)
    context = {
        'form': form,
    }
    return render(request, 'accounts/profile-create.html', context)


def profile_edit(request, pk):
    profile = get_profile_by_pk(pk)
    if request.method == 'GET':
        form = EditProfileForm(instance=profile)
    else:
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile details', profile.user_id)
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'accounts/profile-edit.html', context)
