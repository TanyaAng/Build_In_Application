from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as views

from buildin.common.forms import CreateCommentForm

from buildin.common.models import TaskComment
from buildin.projects.models import BuildInProject

from buildin.repository.account_repository import get_user_full_name, get_request_user_id
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


class DashboardView(LoginRequiredMixin, views.ListView):
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


# FBV for Dashboard
# def dashboard(request):
#     user_full_name = get_full_of_logged_user(request)
#     # get only projects, in which current user is participant
#     projects = BuildInProject.objects.filter(participants__exact=request.user)
#     context = {
#         'projects': projects,
#         'user_full_name': user_full_name,
#     }
#     return render(request, 'projects/dashboard.html', context)


class CommentCreateView(views.CreateView):
    model = TaskComment
    form_class = CreateCommentForm
    template_name = 'tasks/task-comments.html'

    def get_success_url(self):
        return reverse_lazy('project details', kwargs={'build_slug': self.object.to_task.project.slug})

    # def post(self, request, *args, **kwargs):
    #     def post(self, request, *args, **kwargs):
    #         """
    #         Handle POST requests: instantiate a form instance with the passed
    #         POST variables and then check if it's valid.
    #         """
    #         form = self.get_form()
    #         if form.is_valid():
    #             return self.form_valid(form)
    #         else:
    #             return self.form_invalid(form)

    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     self.object = form.save()
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     post = get_object_or_404(Request, slug=self.kwargs['slug'])
    #     Form.instance.post = Request
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     post = get_object_or_404(ProjectTask, slug=self.kwargs['task_slug'])
    #     form.instance.post = ProjectTask
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     comment = super().form_valid(form)
    #     comment.user = self.request.user
    #     comment.save()
    #     return super().form_valid(form)


def comment_task(request, task_slug):
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
            comment.user = request.user
            comment.save()
            return redirect(reverse_lazy('comment section', kwargs={'task_slug': task.slug}))
    context = {
        'form': form,
        'task': task,
        'comments': comments,
        'user_full_name': user_full_name,
    }
    return render(request, 'tasks/task-comments.html', context)
