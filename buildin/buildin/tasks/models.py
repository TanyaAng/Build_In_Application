from django.core.validators import MinValueValidator
from django.db import models

from buildin.accounts.models import BuildInUser
from buildin.projects.models import BuildInProject


class ProjectTask(models.Model):
    TIME_ESTIMATION_MIN_VALUE = 0
    TASK_ID_MAX_LENGTH = 30
    TASK_NAME_MAX_LENGTH = 60

    task_id = models.CharField(
        max_length=TASK_ID_MAX_LENGTH,
    )

    task_name = models.CharField(
        max_length=TASK_NAME_MAX_LENGTH,
    )

    time_estimation = models.FloatField(
        validators=(MinValueValidator(TIME_ESTIMATION_MIN_VALUE),),
        null=True,
        blank=True,
    )

    designer = models.ForeignKey(BuildInUser, related_name='user_designer',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 )
    checked_by = models.ForeignKey(BuildInUser, related_name='user_checker',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True
                                   )

    is_ready_for_markups = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    is_approved = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    is_issued = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    project = models.ForeignKey(
        BuildInProject,
        on_delete=models.RESTRICT,
    )
