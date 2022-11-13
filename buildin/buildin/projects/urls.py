from django.urls import path, include

from buildin.projects.views import project_create, project_details, project_contacts, project_edit, \
    project_delete

urlpatterns = (
    path('add/', project_create, name='project create'),
    path('building/<slug:build_slug>/',
         include([
             path('details/', project_details, name='project details'),
             path('contacts/', project_contacts, name='project contacts'),
             path('edit/', project_edit, name='project edit'),
             path('delete/', project_delete, name='project delete'),
         ])),
    path('building/<slug:build_slug>/', include('buildin.tasks.urls')),
)

# import buildin.common.signals
