from django.contrib import admin
from django.urls import path, include

urlpatterns = (
    path('admin/', admin.site.urls),
    path('', include('buildin.common.urls')),
    path('accounts/', include('buildin.accounts.urls')),
    path('projects/', include('buildin.projects.urls')),
    path('tasks/', include('buildin.tasks.urls')),
    path('departments/', include('buildin.department.urls')),

)
