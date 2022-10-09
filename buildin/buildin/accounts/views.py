from django.contrib.auth import views as auth_views
from django.contrib.auth import logout

from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from django.views.generic import CreateView

from buildin.accounts.forms import CreateProfileForm
from buildin.accounts.models import BuildInUser


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


def user_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home page')


class UserRegisterView(CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'


def profile_details(request, pk):
    return render(request, 'accounts/profile-details.html')


def profile_edit(request, pk):
    return render(request, 'accounts/profile-edit.html')
