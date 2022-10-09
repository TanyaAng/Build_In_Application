from django.contrib.auth import views as auth_views, logout

from django.urls import reverse_lazy
from django.shortcuts import render, redirect

# from buildin.accounts.forms import RegisterForm


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()
    # success_url = reverse_lazy('profile details', kwargs={'pk': 1})
    # success_url = reverse_lazy('dashboard')


# class UserLogoutView(auth_views.LogoutView):
# template_name = 'accounts/logout.html'


def user_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home page')


def user_register(request):
    # if request.method == 'POST':
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('login')
    # else:
    #     form = RegisterForm()
    # context = {
    #     'form': form,
    # }
    return render(request, 'accounts/register.html')


def profile_details(request, pk):
    return render(request, 'accounts/profile-details.html')


def profile_edit(request, pk):
    return render(request, 'accounts/profile-edit.html')
