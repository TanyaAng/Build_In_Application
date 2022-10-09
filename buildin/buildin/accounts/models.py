from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models

from buildin.accounts.managers import BuildInUserManager

# UserModel = get_user_model()


# from AbstractBaseUser we have password field by default
# PermissionsMixins is for django admin access
class BuildInUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):

    email = models.EmailField(
        unique=True,
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    # Set our custom manager to the current model
    objects = BuildInUserManager()


# class Profile(models.Model):
#     CONTRACTOR = 'Contractor'
#     DESIGNER = 'Designer'
#     BUILDER = 'Builder'
#     SUPERVISOR = 'Supervisor'
#     ROLES = [(x, x) for x in [CONTRACTOR, DESIGNER, BUILDER, DESIGNER]]
#     PARTICIPANT_ROLE_MAX_LENGTH = max(len(x) for x, _ in ROLES)
#
#     FIRST_NAME_MAX_LENGTH = 35
#     LAST_NAME_MAX_LENGTH = 35
#
#     first_name = models.CharField(
#         max_length=FIRST_NAME_MAX_LENGTH,
#     )
#
#     last_name = models.CharField(
#         max_length=LAST_NAME_MAX_LENGTH,
#     )
#
#     phone_number = models.TextField(
#         null=True,
#         blank=True,
#     )
#
#     participant_role = models.CharField(
#         max_length=PARTICIPANT_ROLE_MAX_LENGTH,
#         choices=ROLES,
#     )
#
#     user = models.OneToOneField(
#         UserModel,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )
