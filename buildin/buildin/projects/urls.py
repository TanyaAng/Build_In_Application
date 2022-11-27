from django.urls import path, include

from buildin.projects.views import ProjectDetailsView, ProjectCreateView, ProjectUpdateView, \
    project_delete, ProjectContactView

urlpatterns = (
    path('add/', ProjectCreateView.as_view(), name='project create'),
    path('building/<slug:build_slug>/',
         include([
             path('details/', ProjectDetailsView.as_view(), name='project details'),
             path('contacts/', ProjectContactView.as_view(), name='project contacts'),
             path('edit/', ProjectUpdateView.as_view(), name='project edit'),
             path('delete/', project_delete, name='project delete'),
         ])),
    path('building/<slug:build_slug>/', include('buildin.tasks.urls')),
)

# import buildin.common.signals
