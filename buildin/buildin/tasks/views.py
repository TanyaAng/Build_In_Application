from django.shortcuts import render, redirect

from buildin.common.helpers.user_helpers import get_full_name_current_user
from buildin.projects.models import BuildInProject
from buildin.tasks.models import ProjectTask
from buildin.tasks.forms import CreateTaskForm, EditTaskForm, DeleteTaskForm


def task_create(request, pk):
    project = BuildInProject.objects.filter(pk=pk).get()
    if request.method == 'GET':
        form = CreateTaskForm(project=project)
    else:
        form = CreateTaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project details', pk)
    context = {
        'form': form,
        'project': project,
        'user_full_name': get_full_name_current_user(request),
    }
    return render(request, 'tasks/task-create.html', context)


def task_edit(request, pk, task_pk):
    project = BuildInProject.objects.filter(pk=pk).get()
    task = ProjectTask.objects.filter(pk=task_pk).get()
    if request.method == 'GET':
        form = EditTaskForm(instance=task, project=project)
    else:
        form = EditTaskForm(request.POST, instance=task, project=project)
        if form.is_valid():
            form.save()
            return redirect('project details', pk)
    context = {
        'form': form,
        'project': project,
        'task': task,
        'user_full_name': get_full_name_current_user(request),
    }
    return render(request, 'tasks/task-edit.html', context)


def task_delete(request, pk, task_pk):
    project = BuildInProject.objects.filter(pk=pk).get()
    task = ProjectTask.objects.filter(pk=task_pk).get()
    if request.method == 'GET':
        form = DeleteTaskForm(instance=task)
    else:
        form = DeleteTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project details', pk)
    context = {
        'form': form,
        'project': project,
        'task': task,
        'user_full_name': get_full_name_current_user(request),
    }
    return render(request, 'tasks/task-delete.html', context)
