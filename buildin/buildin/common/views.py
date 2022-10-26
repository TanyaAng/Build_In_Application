from django.shortcuts import redirect
from django.views import generic as view

from buildin.common.helpers.user_helpers import get_full_of_logged_user
from buildin.projects.models import BuildInProject


class HomeView(view.TemplateView):
    template_name = 'common/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_full_name = get_full_of_logged_user(request)
            self.get_context_data(kwargs={'user_full_name': user_full_name})
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(view.ListView):
    model = BuildInProject
    template_name = 'common/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_full_name = get_full_of_logged_user(self.request)
        projects = BuildInProject.objects.filter(participants__exact=self.request.user)
        context['user_full_name'] = user_full_name
        context['projects'] = projects
        return context


# FBV for Dashboard
# def dashboard(request):
#     user_full_name = get_full_of_logged_user(request)
#     # get only projects, in which current user is participant
#     projects = BuildInProject.objects.filter(participants__exact=request.user)
#     context = {
#         'projects': projects,
#         'user_full_name': user_full_name,
#     }
#     return render(request, 'projects/dashboard.html', context)
