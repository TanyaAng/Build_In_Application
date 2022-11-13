from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

from buildin.accounts.models import BuildInUser
from buildin.core.models_mixins import ChoiceEnumMixin

UserModel = get_user_model()


class ProjectPhases(ChoiceEnumMixin, Enum):
    RandD = 'Research and Development'
    PD = 'Preliminary Design'
    SD = 'Schematic Design'
    DD = 'Design Development'
    CD = 'Construction Document'
    OTHER = 'Other'


class BuildInProject(models.Model):
    PROJECT_ID_MAX_LENGTH = 40
    #
    # PHASES = (
    #     (RandD, "R&D"),
    #     (PD, "Preliminary design"),
    #     (SD, "Schematic Design"),
    #     (DD, "Design Development"),
    #     (CD, "Construction Documentation"),
    #     (OTHER, 'Other')
    # )
    # PROJECT_PHASE_MAX_LENGTH = max(len(x) for x, _ in PHASES)

    project_identifier = models.CharField(
        max_length=PROJECT_ID_MAX_LENGTH,
    )

    project_name = models.TextField(
        null=True,
        blank=True,
    )

    project_phase = models.CharField(
        max_length=ProjectPhases.max_len(),
        choices=ProjectPhases.choices(),
        null=True,
        blank=True,
    )

    client_name = models.CharField(
        max_length=35,
        null=True,
        blank=True
    )

    date_added = models.DateField(
        auto_now_add=True,
    )

    deadline_date = models.DateField(
        null=True,
        blank=True,
    )

    project_img = models.URLField(
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        editable=False)

    # One to Many Relations
    owner = models.ForeignKey(UserModel, related_name='user', on_delete=models.RESTRICT)

    # Many to Many Relations
    participants = models.ManyToManyField(UserModel)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.project_identifier}-{self.id}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_identifier}"

    class Meta:
        ordering = ('project_identifier',)
