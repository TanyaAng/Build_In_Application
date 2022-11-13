from django.urls import path

from buildin.common.views import HomeView, DashboardView, comment_task

urlpatterns = (
    path('', HomeView.as_view(), name='home page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('comment/<slug:task_slug>/', comment_task, name='add comment')
)
