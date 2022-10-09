from django.contrib import admin

from buildin.projects.models import BuildInProject


@admin.register(BuildInProject)
class BuildInProjectAdmin(admin.ModelAdmin):
    pass
