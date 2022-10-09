from django.shortcuts import render

from buildin.projects.models import BuildInProject


def dashboard(request):
    # get only projects, in which current user is participant
    projects = BuildInProject.objects.filter(participants__exact=request.user)
    context = {
        'projects': projects,
    }
    return render(request, 'projects/dashboard.html', context)


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
