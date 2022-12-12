from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

UserModel = get_user_model()


@admin.register(UserModel)
class BuildInUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    ordering = ('email','is_staff')
    fieldsets = (
        ('User Credentials',
         {'fields': ('email', 'password')}
         ),
        ('Permissions',
         {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }
         ),
        ('Date joined and last login date',
         {'fields': ('last_login', 'date_joined')}
         ),
    )

    # Refers to creation form in django admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('date_joined',)


