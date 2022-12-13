from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from buildin.core.helpers.tasks_helper import calculate_total_time_of_tasks, calculate_days_to_deadline
from buildin.core.repository.task_repository import get_all_tasks_by_project, check_if_task_is_approved
from buildin.core.service.account_service import get_request_user_full_name
from buildin.core.service.project_service import handle_user_perm_to_get_project, \
    handle_user_perm_to_update_project, handle_user_perm_to_delete_project
from buildin.projects.forms import CreateProjectForm, EditProjectForm, DeleteProjectForm
from buildin.projects.models import BuildInProject

from buildin.core.repository.project_repository import get_project_by_slug, get_project_participants


class ProjectCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = BuildInProject
    form_class = CreateProjectForm
    template_name = 'projects/project-create.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_full_name'] = get_request_user_full_name(self.request)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)


class ProjectDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = BuildInProject
    template_name = 'projects/project-details.html'
    slug_url_kwarg = 'build_slug'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_full_name = get_request_user_full_name(self.request)
        tasks = get_all_tasks_by_project(self.object)
        total_time_of_project = calculate_total_time_of_tasks(tasks)
        left_tasks=[task for task in tasks if not check_if_task_is_approved(task)]
        total_time_of_left_tasks = calculate_total_time_of_tasks(left_tasks)
        days_to_deadline = calculate_days_to_deadline(self.object.deadline_date)

        context['tasks'] = tasks
        context['total_time_of_project'] = total_time_of_project
        context['total_time_of_left_tasks'] = total_time_of_left_tasks
        context['user_full_name'] = user_full_name
        context['days_to_deadline'] = days_to_deadline
        return context

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        handle_user_perm_to_get_project(request=self.request, project=project)
        return super().dispatch(request, *args, **kwargs)


class ProjectUpdateView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = BuildInProject
    form_class = EditProjectForm
    slug_url_kwarg = 'build_slug'
    context_object_name = 'project'
    template_name = 'projects/project-edit.html'

    def get_success_url(self):
        return reverse_lazy('project details', kwargs={'build_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_full_name'] = get_request_user_full_name(self.request)
        return context


    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        handle_user_perm_to_update_project(request=self.request, project=project)
        return super().dispatch(request, *args, **kwargs)


@login_required
def project_delete(request, build_slug):
    project = get_project_by_slug(build_slug)
    handle_user_perm_to_delete_project(request=request, project=project)

    if request.method == 'GET':
        form = DeleteProjectForm(instance=project)
    else:
        form = DeleteProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home page')
    user_full_name = get_request_user_full_name(request)
    context = {
        'form': form,
        'project': project,
        'user_full_name': user_full_name,
    }
    return render(request, 'projects/project-delete.html', context)


class ProjectContactView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = BuildInProject
    template_name = 'projects/project-contacts.html'
    slug_url_kwarg = 'build_slug'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participants = get_project_participants(self.object)

        if participants:
            context['participants'] = participants
            context['user_full_name'] = get_request_user_full_name(self.request)
        return context

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        handle_user_perm_to_get_project(request=self.request, project=project)
        return super().dispatch(request, *args, **kwargs)
