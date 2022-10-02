from django.urls import path, include

from buildin.tasks.views import task_create, task_edit, task_delete

urlpatterns = (
    path('add/', task_create, name='task create'),
    path('<int:pk>/',
         include([
             path('edit/', task_edit, name='task edit'),
             path('delete/', task_delete, name='task delete'),
         ])),
)