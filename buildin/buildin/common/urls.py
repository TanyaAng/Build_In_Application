from django.urls import path

from buildin.common.views import HomeView, DashboardView, comment_task_create, LogActivityView

urlpatterns = (
    path('', HomeView.as_view(), name='home page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logactivity/', LogActivityView.as_view(), name='log activity'),
    path('comment/<slug:task_slug>/', comment_task_create, name='comment section')
)
