from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins
from django.http import Http404
from django.views import generic as views
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect

from buildin.accounts.models import Profile
from buildin.repository.account_repository import get_user_full_name, get_user_by_profile, get_request_user
from buildin.repository.project_repository import get_user_projects_where_user_is_participant_or_owner

from buildin.repository.task_repository import get_user_tasks

from buildin.accounts.forms import UserRegistrationForm, EditProfileForm, CreateProfileForm

UserModel = auth_views.get_user_model()


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutView(auth_views.LogoutView):
    # Logout success url is set in Setting.py
    pass


class UserRegisterView(views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        # custom logic - login automatically after registration
        user = self.object
        request = self.request
        login(request, user)
        return result


class ProfileDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        try:
            self.get_object()
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('profile create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = get_user_by_profile(self.object)
        user_full_name = get_user_full_name(self.request)
        user_projects = get_user_projects_where_user_is_participant_or_owner(user)
        user_tasks = get_user_tasks(user)

        context['user_full_name'] = user_full_name
        context['user_projects'] = user_projects
        context['user_task'] = user_tasks

        return context


class ProfileCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'accounts/profile-create.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

    def form_valid(self, form):
        form.instance.user = get_request_user(self.request)
        form.save()
        return super().form_valid(form)


class ProfileUpdateView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context
