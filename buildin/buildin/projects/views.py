from django.shortcuts import render


def dashboard(request):
    return render(request, 'projects/dashboard.html')


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
