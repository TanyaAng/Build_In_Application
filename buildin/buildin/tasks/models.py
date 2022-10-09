from django.db import models

from buildin.accounts.models import BuildInUser
from buildin.projects.models import BuildInProject


class ProjectTask(models.Model):
    TASK_ID_MAX_LENGTH=30
    TASK_NAME_MAX_LENGTH=60

    task_id = models.CharField(
        max_length=TASK_ID_MAX_LENGTH,
        # unique=True,
    )

    task_name = models.CharField(
        max_length=TASK_NAME_MAX_LENGTH,
    )

    time_estimation = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    project = models.ForeignKey(
        BuildInProject,
        on_delete=models.SET_NULL,
        null=True)

    # designer = models.ManyToManyField(BuildInUser)

    # approved_by=models.ManyToManyField(BuildInUser)

    # approved_by = models.ManyToManyField(to=BuildInProject.project_leaders)

    is_ready_for_markups = models.BooleanField()

    is_approved = models.BooleanField()

    is_issued = models.BooleanField()
