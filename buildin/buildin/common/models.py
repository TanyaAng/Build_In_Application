from django.contrib.auth import get_user_model
from django.db import models

from buildin.accounts.models import BuildInUser
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

