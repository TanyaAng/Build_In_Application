from django.contrib import admin
from django.urls import path, include

from buildin.common.views import custom_handler403, custom_handler404, custom_handler500

urlpatterns = (
    path('admin/', admin.site.urls),
    path('', include('buildin.common.urls')),
    path('accounts/', include('buildin.accounts.urls')),
    path('projects/', include('buildin.projects.urls')),
)

handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500
