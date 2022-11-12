from enum import Enum

from buildin.accounts.managers import BuildInUserManager

from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User

from phone_field import PhoneField

from buildin.core.models_mixins import ChoiceEnumMixin


class ParticipantRole(ChoiceEnumMixin, Enum):
    CONTRACTOR = 'Contractor'
    DESIGNER = 'Designer'
    BUILDER = 'Builder'
    SUPERVISOR = 'Supervisor'


class BuildInUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    objects = BuildInUserManager()
    USERNAME_FIELD = 'email'


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 35
    LAST_NAME_MAX_LENGTH = 35
    PASSWORD_MAX_LENGTH = 50

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
    )

    phone_number = PhoneField(
        null=True,
        blank=True,
        E164_only=False,
        # unique=True,
    )

    participant_role = models.CharField(
        max_length=ParticipantRole.max_len(),
        choices=ParticipantRole.choices(),
    )

    user = models.OneToOneField(
        BuildInUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name
