from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from buildin.repository.account_repository import get_user_full_name
from buildin.repository.project_repository import get_project_by_slug
from buildin.repository.task_repository import get_task_by_slug

from buildin.tasks.forms import CreateTaskForm, EditTaskForm, DeleteTaskForm



@login_required
def task_create(request, build_slug):
    project = get_project_by_slug(build_slug)
    if request.method == 'GET':
        form = CreateTaskForm(project=project)
    else:
        form = CreateTaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project details', build_slug)
    context = {
        'form': form,
        'project': project,
        'user_full_name': get_user_full_name(request),
    }
    return render(request, 'tasks/task-create.html', context)


@login_required
def task_edit(request, build_slug, task_slug):
    project = get_project_by_slug(build_slug)
    task = get_task_by_slug(task_slug)
    if request.method == 'GET':
        form = EditTaskForm(instance=task, project=project)
    else:
        form = EditTaskForm(request.POST, instance=task, project=project)
        if form.is_valid():
            form.save()
            return redirect('project details', build_slug)
    context = {
        'form': form,
        'project': project,
        'task': task,
        'user_full_name': get_user_full_name(request),
    }
    return render(request, 'tasks/task-edit.html', context)


@login_required
def task_delete(request, build_slug, task_slug):
    project = get_project_by_slug(build_slug)
    task = get_task_by_slug(task_slug)
    if request.method == 'GET':
        form = DeleteTaskForm(instance=task)
    else:
        form = DeleteTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project details', build_slug)
    context = {
        'form': form,
        'project': project,
        'task': task,
        'user_full_name': get_user_full_name(request),
    }
    return render(request, 'tasks/task-delete.html', context)
