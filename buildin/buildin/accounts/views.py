from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins

from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect

from buildin.accounts.models import Profile
from buildin.core.app_groups.app_groups import set_user_to_regular_user_group

from buildin.core.helpers.tasks_helper import calculate_total_time_of_tasks
from buildin.core.repository.account_repository import get_user_id_by_profile, get_request_user, \
    get_profile_of_current_user

from buildin.core.repository.project_repository import get_user_projects_where_user_is_participant_or_owner

from buildin.accounts.forms import UserRegistrationForm, EditProfileForm, CreateProfileForm
from buildin.core.repository.task_repository import get_user_tasks_to_design, get_user_tasks_to_check
from buildin.core.service.account_service import get_request_user_full_name, if_request_user_is_owner_of_profile, \
    login_after_registration

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

        user = self.object
        set_user_to_regular_user_group(user)

        login_after_registration(self.request, user)
        return result


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
        user_full_name = get_request_user_full_name(self.request)
        context['user_full_name'] = user_full_name
        return context


class ProfileDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = get_user_id_by_profile(self.object)
        user_full_name = get_request_user_full_name(self.request)
        user_projects = get_user_projects_where_user_is_participant_or_owner(user)
        tasks_to_design = get_user_tasks_to_design(user)
        tasks_to_check = get_user_tasks_to_check(user)
        total_time_of_tasks_to_design = calculate_total_time_of_tasks(tasks_to_design)

        context['user_full_name'] = user_full_name
        context['user_projects'] = user_projects
        context['user_designer_tasks'] = tasks_to_design
        context['user_checker_tasks'] = tasks_to_check
        context['total_time_of_tasks_to_design'] = total_time_of_tasks_to_design
        return context

    def dispatch(self, request, *args, **kwargs):
        profile_of_logged_user = get_profile_of_current_user(self.request)
        if not profile_of_logged_user:
            return redirect('profile create')
        if profile_of_logged_user != self.get_object():
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['profile'] = profile
        return context

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if not if_request_user_is_owner_of_profile(self.request, profile):
            return redirect('profile details', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)
