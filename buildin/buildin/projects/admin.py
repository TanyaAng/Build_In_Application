from django.contrib import admin

from buildin.projects.models import BuildInProject


@admin.register(BuildInProject)
class BuildInProjectAdmin(admin.ModelAdmin):
    list_display = ('project_identifier', 'owner', 'deadline_date')
    ordering = ('project_identifier', 'owner', 'deadline_date')
