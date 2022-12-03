from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from buildin.core.helpers.tasks_helper import calculate_total_time_of_project, calculate_days_to_deadline
from buildin.projects.forms import CreateProjectForm, EditProjectForm, DeleteProjectForm
from buildin.projects.models import BuildInProject

from buildin.repository.project_repository import get_project_by_slug, get_project_participants
from buildin.repository.task_repository import get_all_tasks_by_project
from buildin.service.account_service import handle_user_permissions_to_object, get_user_full_name


class ProjectDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = BuildInProject
    template_name = 'projects/project-details.html'
    slug_url_kwarg = 'build_slug'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_full_name = get_user_full_name(self.request)
        project_participants = get_project_participants(self.object)
        participants = [p.email for p in project_participants]
        tasks = get_all_tasks_by_project(self.object)
        total_time_of_project = calculate_total_time_of_project(tasks)
        days_to_deadline = calculate_days_to_deadline(self.object.deadline_date)

        context['tasks'] = tasks
        context['total_time_of_project'] = total_time_of_project
        context['user_full_name'] = user_full_name
        context['participants'] = ', '.join(participants)
        context['days_to_deadline'] = days_to_deadline
        return context

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        participants = get_project_participants(object)
        handle_user_permissions_to_object(request=self.request, object=object, participants=participants)
        return super().dispatch(request, *args, **kwargs)


class ProjectCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = BuildInProject
    form_class = CreateProjectForm
    template_name = 'projects/project-create.html'
    success_url = reverse_lazy('home page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_full_name'] = get_user_full_name(self.request)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)


class ProjectUpdateView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = BuildInProject
    form_class = EditProjectForm
    slug_url_kwarg = 'build_slug'
    context_object_name = 'project'
    template_name = 'projects/project-edit.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_full_name'] = get_user_full_name(self.request)
        return context

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        participants = get_project_participants(object)
        handle_user_permissions_to_object(request=self.request, object=object, participants=participants)
        return super().dispatch(request, *args, **kwargs)


# TODO CLASS BASED VIEW do not show the current project in form

# class ProjectDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
#     model = BuildInProject
#     form_class = DeleteProjectForm
#
#     slug_url_kwarg = 'build_slug'
#     context_object_name = 'project'
#
#     template_name = 'projects/project-delete.html'
#     success_url = reverse_lazy('dashboard')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_full_name'] = get_user_full_name(self.request)
#         return context


@login_required
def project_delete(request, build_slug):
    project = get_project_by_slug(build_slug)
    participants = get_project_participants(project)
    handle_user_permissions_to_object(request=request, object=project, participants=participants)

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


class ProjectContactView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = BuildInProject
    template_name = 'projects/project-contacts.html'
    slug_url_kwarg = 'build_slug'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_participants = get_project_participants(self.object)

        if project_participants:
            participants = [p.email for p in project_participants]
            context['participants'] = ', '.join(participants)
            context['project_participants'] = project_participants
        return context

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        participants = get_project_participants(object)
        handle_user_permissions_to_object(request=self.request, object=object, participants=participants)
        return super().dispatch(request, *args, **kwargs)
