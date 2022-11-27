from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from buildin.common.forms import CreateCommentForm
from buildin.common.models import LogActivity
from buildin.projects.models import BuildInProject

from buildin.repository.account_repository import get_user_full_name, get_request_user, get_request_user_id
from buildin.repository.common_repository import get_all_comments_to_task
from buildin.repository.project_repository import get_user_projects_where_user_is_participant_or_owner, get_all_projects
from buildin.repository.task_repository import get_task_by_slug



class HomeView(views.TemplateView):
    template_name = 'common/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_full_name = get_user_full_name(self.request)
        context['user_full_name'] = user_full_name
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = BuildInProject
    template_name = 'common/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_full_name = get_user_full_name(self.request)
        user_id = get_request_user_id(self.request)
        if not self.request.user.is_superuser:
            self.object_list = get_user_projects_where_user_is_participant_or_owner(user_id)
            projects = self.object_list
        else:
            projects = get_all_projects()
        context['user_full_name'] = user_full_name
        context['projects'] = projects
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


@login_required
def comment_task_create(request, task_slug):
    task = get_task_by_slug(task_slug)
    comments = get_all_comments_to_task(task)
    user_full_name = get_user_full_name(request)
    if request.method == 'GET':
        form = CreateCommentForm()
    else:
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_task = task
            comment.user = get_request_user(request)
            comment.save()
            return redirect(reverse_lazy('comment section', kwargs={'task_slug': task.slug}))
    context = {
        'form': form,
        'task': task,
        'comments': comments,
        'user_full_name': user_full_name,
    }
    return render(request, 'tasks/task-comments.html', context)


# TODO comment_task_edit and comment_task_delete_view

class LogActivityView(auth_mixins.LoginRequiredMixin,auth_mixins.PermissionRequiredMixin, views.ListView):
    model = LogActivity
    template_name = 'common/log-activity.html'
    context_object_name = 'comments'
    permission_required = 'common.view_logactivity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_full_name'] = get_user_full_name(self.request)
        return context

    def handle_no_permission(self):
        return render(self.request, '403.html')

