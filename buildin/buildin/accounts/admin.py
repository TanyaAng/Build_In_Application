from django.contrib import admin

from buildin.accounts.models import BuildInUser


@admin.register(BuildInUser)
class UserAdmin(admin.ModelAdmin):
    pass
