from buildin.accounts.managers import BuildInUserManager

from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User

from phone_field import PhoneField


class BuildInUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = BuildInUserManager()


class Profile(models.Model):
    CONTRACTOR = 'Contractor'
    DESIGNER = 'Designer'
    BUILDER = 'Builder'
    SUPERVISOR = 'Supervisor'
    ROLES = [(x, x) for x in [CONTRACTOR, DESIGNER, BUILDER, DESIGNER]]
    PARTICIPANT_ROLE_MAX_LENGTH = max(len(x) for x, _ in ROLES)

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
    )

    participant_role = models.CharField(
        max_length=PARTICIPANT_ROLE_MAX_LENGTH,
        choices=ROLES,
    )

    user = models.OneToOneField(
        BuildInUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
