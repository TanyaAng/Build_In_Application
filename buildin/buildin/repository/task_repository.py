from django.db.models import Q

from buildin.tasks.models import ProjectTask


def get_task_by_slug(task_slug):
    task = ProjectTask.objects.filter(slug=task_slug)
    return task.get()


def get_all_tasks_by_project(project):
    return ProjectTask.objects.filter(project__exact=project)


def get_user_tasks(user):
    user_tasks = ProjectTask.objects.filter(Q(designer__exact=user) | Q(checked_by__exact=user))
    return user_tasks
