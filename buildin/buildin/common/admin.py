from django.contrib import admin

from buildin.common.models import TaskComment, LogActivity


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('to_task', 'user')
    ordering = ('to_task', 'user')
    readonly_fields = ('to_task', 'user')


@admin.register(LogActivity)
class LogActivityAdmin(admin.ModelAdmin):
    list_display = ('publication_date_time', 'user', 'action', 'model', 'to_related' )
    ordering = ('publication_date_time', 'user')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
