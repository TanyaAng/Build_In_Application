from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from buildin.core.helpers.tasks_helper import calculate_total_time_of_project
from buildin.projects.forms import CreateProjectForm, EditProjectForm, DeleteProjectForm
from buildin.repository.account_repository import get_user_full_name
from buildin.repository.project_repository import get_project_by_slug, get_project_participants
from buildin.repository.task_repository import get_all_tasks_by_project



@login_required
def project_details(request, build_slug):
    project = get_project_by_slug(build_slug)
    project_participants = get_project_participants(project)
    participants = [p.email for p in project_participants]
    tasks = get_all_tasks_by_project(project)
    total_time_of_project = calculate_total_time_of_project(tasks)

    context = {
        'project': project,
        'tasks': tasks,
        'total_time_of_project': total_time_of_project,
        'user_full_name': get_user_full_name(request),
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
        'user_full_name': get_user_full_name(request),
    }
    return render(request, 'projects/project-create.html', context)


@login_required
def project_edit(request, build_slug):
    project = get_project_by_slug(build_slug)
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
        'user_full_name': get_user_full_name(request)
    }
    return render(request, 'projects/project-edit.html', context)


@login_required
def project_delete(request, build_slug):
    project = get_project_by_slug(build_slug)
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
        'user_full_name': get_user_full_name(request)
    }
    return render(request, 'projects/project-delete.html', context)

@login_required
def project_contacts(request, build_slug):
    return render(request, 'projects/project-contacts.html')
