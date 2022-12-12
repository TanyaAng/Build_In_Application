from enum import Enum

from buildin.accounts.managers import BuildInUserManager

from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User

from phone_field import PhoneField

from buildin.core.mixins.choice_mixins import ChoiceEnumMixin


class ParticipantRole(ChoiceEnumMixin, Enum):
    INTERN = 'Intern design engineer'
    JN_ENG = 'Junior design engineer'
    MID_ENG = 'Mid design engineer'
    SN_ENG = 'Senior design engineer'
    LEAD = 'Team Lead'


class BuildInUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)

    objects = BuildInUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name='user'


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

    def __str__(self):
        return self.full_name
