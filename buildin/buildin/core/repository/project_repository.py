from django.db.models import Q

from buildin.projects.models import BuildInProject


def get_all_projects():
    return BuildInProject.objects.all()


def get_project_by_slug(build_slug):
    project = BuildInProject.objects.filter(slug=build_slug)
    return project.get()


def get_project_participants(project):
    return project.participants.all()


def get_project_owner(project):
    return project.owner


def get_user_projects_where_user_is_participant_or_owner(user_id):
    user_projects = BuildInProject.objects.filter(
        Q(participants__exact=user_id) |
        Q(owner_id=user_id)
    )
    return user_projects.distinct()


def get_project_related_to_task(task):
    project = BuildInProject.objects.filter(projecttask__exact=task)
    return project.get()
