from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models

from buildin.accounts.models import BuildInUser
from buildin.core.models_mixins import ChoiceEnumMixin
from buildin.projects.models import BuildInProject
from buildin.tasks.models import ProjectTask

UserModel = get_user_model()


class TaskComment(models.Model):
    DESC_MAX_LENGTH = 300

    description = models.CharField(
        max_length=DESC_MAX_LENGTH,
    )

    publication_date_time = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    to_task = models.ForeignKey(to=ProjectTask, on_delete=models.CASCADE)

    user = models.ForeignKey(to=UserModel, on_delete=models.RESTRICT)

    class Meta:
        ordering = ['-publication_date_time']


class LogActivity(models.Model):
    ACTION_CR_UP = 'create/update comment'
    ACTION_DEL = 'delete comment'

    user_id = models.IntegerField()

    action = models.CharField(
        max_length=max(len(ACTION_CR_UP), len(ACTION_DEL)),
    )

    model = models.CharField(
        max_length=max(BuildInProject.PROJECT_ID_MAX_LENGTH, ProjectTask.TASK_ID_MAX_LENGTH)
    )

    to_related = models.CharField(
        max_length=max(BuildInProject.PROJECT_ID_MAX_LENGTH, ProjectTask.TASK_ID_MAX_LENGTH)
    )

    publication_date_time = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
