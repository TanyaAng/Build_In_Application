from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as auth_models

from buildin.accounts.managers import BuildInUserManager

#from AbstractBaseUser we have password field by default
#PermissionsMixins is for django admin access

class BuildInUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    # Set our custom manager to the current model
    objects = BuildInUserManager()
