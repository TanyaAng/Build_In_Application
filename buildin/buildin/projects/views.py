from django.shortcuts import render
from django.views import generic as views

from buildin.accounts.models import Profile
from buildin.common.helpers.user_helpers import get_full_of_logged_user
from buildin.projects.models import BuildInProject


class DashboardView(views.ListView):
    model = BuildInProject
    template_name = 'projects/dashboard.html'

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


def project_create(request):
    return render(request, 'projects/project-create.html')


def project_details(request, pk, project_name):
    return render(request, 'projects/project-details.html')


def project_contacts(request, pk, project_name):
    return render(request, 'projects/project-contacts.html')


def project_edit(request, pk, project_name):
    return render(request, 'projects/project-edit.html')


def project_delete(request, pk, project_name):
    return render(request, 'projects/project-delete.html')
