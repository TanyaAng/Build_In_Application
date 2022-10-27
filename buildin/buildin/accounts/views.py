from django.db.models import Q

from django.contrib.auth import views as auth_views
from django.views import generic as views
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import render

from buildin.common.helpers.user_helpers import get_profile_of_current_user
from buildin.projects.models import BuildInProject
from buildin.tasks.models import ProjectTask
from buildin.accounts.forms import UserRegistrationForm


UserModel = auth_views.get_user_model()


class UserRegisterView(views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/profile_create.html'
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


class ProfileDetailsView(views.DetailView):
    model = UserModel
    template_name = 'accounts/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_projects=BuildInProject.objects.filter(
            Q(participants__in=[self.request.user.id]) |
            Q(owner_id=self.request.user.id)
        )
        user_tasks = ProjectTask.objects.filter(
            Q(designer__exact=self.request.user) | Q(checked_by__exact=self.request.user))

        context['profile'] = get_profile_of_current_user(self.request)
        context['user_projects'] = user_projects.distinct()
        print(user_projects)
        context['user_tasks'] = user_tasks
        return context


# def profile_details(request, pk):
#     user_projects = BuildInProject.objects.filter(participants__exact=request.user.id)
#     context = {
#         'profile': get_profile_of_current_user(request),
#         'user_full_name': get_full_of_logged_user(request),
#         'user_email': request.user,
#         'user_projects': user_projects
#     }
#     return render(request, 'accounts/profile-details.html', context)


def profile_edit(request, pk):
    return render(request, 'accounts/profile-edit.html')
