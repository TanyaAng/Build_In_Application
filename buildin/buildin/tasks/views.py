from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from buildin.repository.account_repository import get_user_full_name
from buildin.repository.project_repository import get_project_by_slug
from buildin.repository.task_repository import get_task_by_slug

from buildin.tasks.forms import CreateTaskForm, EditTaskForm, DeleteTaskForm
from buildin.tasks.models import ProjectTask


# class TaskCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
#     model = ProjectTask
#     form_class = CreateTaskForm
#
#     template_name = 'tasks/task-create.html'
#     slug_url_kwarg = 'build_slug'
#
#     def get(self, request, *args, **kwargs):
#         print(request)
#         # kwargs['project'] = self.object.project
#         return super().get(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse_lazy('profile details', kwargs={'build_slug': self.object.project.slug})
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['project'] = self.object.project
#         context['user_full_name'] = get_user_full_name(self.request)
#         return context
#
#     def form_valid(self, form):
#         form.instance.project = self.object.project
#         form.save()
#         return super().form_valid(form)


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
