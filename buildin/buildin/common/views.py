from django.db.models import Q
from django.shortcuts import redirect
from django.views import generic as view

from buildin.common.helpers.user_helpers import get_full_name_current_user
from buildin.projects.models import BuildInProject



class HomeView(view.TemplateView):
    template_name = 'common/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_full_name = get_full_name_current_user(request)
            self.get_context_data(kwargs={'user_full_name': user_full_name})
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(view.ListView):
    model = BuildInProject
    template_name = 'common/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_full_name = get_full_name_current_user(self.request)
        BuildInProject.objects.filter(
            Q(participants__in=[self.request.user.id]) |
            Q(owner_id=self.request.user.id)
        )
        # self.object_list saves the proper QuerySet
        projects = self.object_list
        context['user_full_name'] = user_full_name
        context['projects'] = projects
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

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
