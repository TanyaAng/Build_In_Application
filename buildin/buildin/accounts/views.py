from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins

from django.http import Http404
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect

from buildin.accounts.models import Profile
from buildin.core.app_groups import set_user_to_regular_user_group
from buildin.core.helpers.tasks_helper import calculate_total_time_of_tasks
from buildin.repository.account_repository import get_user_by_profile, get_request_user
from buildin.repository.project_repository import get_user_projects_where_user_is_participant_or_owner
from buildin.repository.task_repository import get_user_tasks, get_user_tasks_to_design, get_user_tasks_to_check

from buildin.accounts.forms import UserRegistrationForm, EditProfileForm, CreateProfileForm
from buildin.service.account_service import get_user_full_name

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

        # login automatically after registration
        user = self.object
        set_user_to_regular_user_group(user)
        request = self.request
        login(request, user)
        return result


class ProfileDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = get_user_by_profile(self.object)
        user_full_name = get_user_full_name(self.request)
        user_projects = get_user_projects_where_user_is_participant_or_owner(user)
        tasks_to_design = get_user_tasks_to_design(user)
        tasks_to_check = get_user_tasks_to_check(user)
        total_time_of_tasks_to_design = calculate_total_time_of_tasks(tasks_to_design)

        context['user_full_name'] = user_full_name
        context['user_projects'] = user_projects
        context['user_designer_tasks'] = tasks_to_design
        context['user_checker_tasks'] = tasks_to_check
        context['total_time_of_tasks_to_design']=total_time_of_tasks_to_design
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            object = self.get_object()
            if not self.request.user.pk == object.user_id:
                return redirect('profile details', pk=self.request.user.pk)
            return super().dispatch(request, *args, **kwargs)

        except Http404:
            return redirect('profile create')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_full_name = get_user_full_name(self.request)
        context['user_full_name'] = user_full_name
        return context


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

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if not self.request.user.pk == object.user_id:
            return redirect('profile edit', pk=self.request.user.pk)
        return super().dispatch(request, *args, **kwargs)
