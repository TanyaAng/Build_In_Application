from django.contrib import admin

from buildin.tasks.models import ProjectTask


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'project')
    ordering = ('project',)

