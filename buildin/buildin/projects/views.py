from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from buildin.core.helpers.tasks_helper import calculate_total_time_of_project
from buildin.core.helpers.user_helpers import get_full_name_current_user
from buildin.projects.forms import CreateProjectForm, EditProjectForm, DeleteProjectForm
from buildin.projects.models import BuildInProject
from buildin.tasks.models import ProjectTask


@login_required
def project_details(request, build_slug):
    project = BuildInProject.objects.filter(slug=build_slug).get()
    project_participants = project.participants.all()
    participants = [p.email for p in project_participants]
    tasks = ProjectTask.objects.filter(project__exact=project)
    total_time_of_project = calculate_total_time_of_project(tasks)

    context = {
        'project': project,
        'tasks': tasks,
        'total_time_of_project': total_time_of_project,
        'user_full_name': get_full_name_current_user(request),
        'participants': ', '.join(participants),
    }
    return render(request, 'projects/project-details.html', context)


@login_required
def project_create(request):
    if request.method == 'GET':
        form = CreateProjectForm()
    else:
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('home page')
    context = {
        'form': form,
        'user_full_name': get_full_name_current_user(request),
    }
    return render(request, 'projects/project-create.html', context)


@login_required
def project_edit(request, build_slug):
    project = BuildInProject.objects.filter(slug=build_slug).get()
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


@login_required
def project_delete(request, build_slug):
    project = BuildInProject.objects.filter(slug=build_slug).get()
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

@login_required
def project_contacts(request, build_slug):
    return render(request, 'projects/project-contacts.html')
