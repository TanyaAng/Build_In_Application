from django.db import models

from buildin.accounts.models import BuildInUser


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
        default='https://unsplash.com/photos/VYqkeRANz90',
    )

    participants = models.ManyToManyField(BuildInUser)

    def __str__(self):
        return f"{self.project_identifier}"
