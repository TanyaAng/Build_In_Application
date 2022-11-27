from django.contrib.auth import get_user_model
from django.db import models

from buildin.accounts.models import BuildInUser
from buildin.core.helpers.crud_mapper import get_crud_mapper
from buildin.core.helpers.signals_helper import get_signals_models_related
from buildin.projects.models import BuildInProject
from buildin.tasks.models import ProjectTask

UserModel = get_user_model()


class TaskComment(models.Model):
    DESC_MAX_LENGTH = 300

    description = models.TextField(
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
    CRUD = get_crud_mapper()
    SIGNAL_MODELS_RELATED = get_signals_models_related()

    user = models.EmailField()

    action = models.CharField(
        max_length=max([len(value) for _, value in CRUD.items()]) + max(
            [len(value) for _, value in SIGNAL_MODELS_RELATED.items()]),
    )

    model = models.CharField(
        max_length=max(BuildInProject.PROJECT_ID_MAX_LENGTH, (ProjectTask.TASK_ID_MAX_LENGTH+ProjectTask.TASK_NAME_MAX_LENGTH))
    )

    to_related = models.CharField(
        max_length=max(BuildInProject.PROJECT_ID_MAX_LENGTH, (ProjectTask.TASK_ID_MAX_LENGTH+ProjectTask.TASK_NAME_MAX_LENGTH))
    )

    publication_date_time = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.publication_date_time}: {self.user} {self.action} {self.model} to {self.to_related}"
