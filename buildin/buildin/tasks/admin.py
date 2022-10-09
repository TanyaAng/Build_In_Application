from django.contrib import admin

from buildin.tasks.models import ProjectTask


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'task_id', 'task_name')
    sortable_by = ('project', 'task_id')
