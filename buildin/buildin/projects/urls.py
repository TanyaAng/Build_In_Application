from django.urls import path, include

from buildin.projects.views import DashboardView, project_create, project_details, project_contacts, project_edit, \
    project_delete

urlpatterns = (
    path('', DashboardView.as_view(), name='dashboard'),
    path('add/', project_create, name='project create'),
    path('<int:pk>/buidling/<slug:project_name>/',
         include([
             path('details/', project_details, name='project details'),
             path('contacts/', project_contacts, name='project contacts'),
             path('edit/', project_edit, name='project edit'),
             path('delete/', project_delete, name='project delete'),
         ])),
)