from django.contrib.auth import get_user_model
from django.db import models

from buildin.accounts.models import BuildInUser

UserModel = get_user_model()


class BuildInProject(models.Model):
    PROJECT_ID_MAX_LENGTH = 40
    RandD = 'RD'
    PD = 'PD'
    SD = 'SD'
    DD = 'DD'
    CD = 'CD'
    OTHER = 'Other'
    PHASES = (
        (RandD, "R&D"),
        (PD, "Preliminary design"),
        (SD, "Schematic Design"),
        (DD, "Design Development"),
        (CD, "Construction Documentation"),
        (OTHER, 'Other')
    )
    PROJECT_PHASE_MAX_LENGTH = max(len(x) for x, _ in PHASES)

    project_identifier = models.CharField(
        max_length=PROJECT_ID_MAX_LENGTH,
    )

    project_name = models.TextField(
        null=True,
        blank=True,
    )

    project_phase = models.CharField(
        max_length=PROJECT_PHASE_MAX_LENGTH,
        choices=PHASES,
        default=PD,
    )

    client_name = models.CharField(
        max_length=35,
        null=True,
        blank=True
    )

    deadline_date = models.DateField(
        null=True,
        blank=True,
    )

    project_img = models.URLField(
        default='https://images.unsplash.com/photo-1664819485266-2de9be49b054?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=564&q=80',
    )


    participants = models.ManyToManyField(UserModel)

    def __str__(self):
        return f"{self.project_identifier}"
