from django.shortcuts import render, redirect

from buildin.common.helpers.user_helpers import get_full_name_current_user
from buildin.projects.forms import CreateProjectForm, EditProjectForm, DeleteProjectForm
from buildin.projects.models import BuildInProject


def project_details(request, pk):
    project = BuildInProject.objects.filter(pk=pk).get()
    project_participants = project.participants.all()
    participants = [p.email for p in project_participants]
    context = {
        'project': project,
        'user_full_name': get_full_name_current_user(request),
        'participants': ', '.join(participants)
    }
    return render(request, 'projects/project-details.html', context)


def project_create(request):
    if request.method == 'GET':
        form = CreateProjectForm()
    else:
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner = request.user
            # project = form.save()
            # project.participants.add(request.user)
            project.save()
            return redirect('home page')
    context = {
        'form': form,
        'user_full_name': get_full_name_current_user(request),
    }
    return render(request, 'projects/project-create.html', context)


def project_edit(request, pk):
    project = BuildInProject.objects.filter(pk=pk).get()
    if request.method == 'GET':
        form = EditProjectForm(instance=project)
    else:
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form,
        'project': project,
        'user_full_name': get_full_name_current_user(request)
    }
    return render(request, 'projects/project-edit.html', context)


def project_delete(request, pk):
    project = BuildInProject.objects.filter(pk=pk).get()
    if request.method == 'GET':
        form = DeleteProjectForm(instance=project)
    else:
        form = DeleteProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home page')
    context = {
        'form': form,
        'project': project,
        'user_full_name': get_full_name_current_user(request)
    }
    return render(request, 'projects/project-delete.html', context)


def project_contacts(request, pk):
    return render(request, 'projects/project-contacts.html')
