from django.db.models import Q

from buildin.tasks.models import ProjectTask


def get_all_tasks_by_project(project):
    return ProjectTask.objects.filter(project__exact=project)


def get_task_by_slug(task_slug):
    task = ProjectTask.objects.filter(slug=task_slug)
    return task.get()


def get_user_tasks(user):
    user_tasks = ProjectTask.objects.filter(Q(designer__exact=user) | Q(checked_by__exact=user))
    return user_tasks


def get_user_tasks_to_design(user):
    return ProjectTask.objects.filter(Q(designer__exact=user), Q(is_approved=False))


def get_user_tasks_to_check(user):
    return ProjectTask.objects.filter(Q(checked_by__exact=user), Q(is_issued=False))


def check_if_task_is_approved(task):
    if task.is_approved:
        return True
    return False

def get_task_time_estimation (task):
    return task.time_estimation