from django.contrib import admin
from django.urls import path, include

urlpatterns = (
    path('admin/', admin.site.urls),
    path('', include('buildin.common.urls')),
    path('accounts/', include('buildin.accounts.urls')),
    path('projects/', include('buildin.projects.urls')),
)
