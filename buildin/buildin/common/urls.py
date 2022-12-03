from django.urls import path, include

from buildin.common.views import HomeView, DashboardView, comment_task_create, LogActivityView, CommentEditView, \
comment_delete_view

urlpatterns = (
    path('', HomeView.as_view(), name='home page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logactivity/', LogActivityView.as_view(), name='log activity'),
    path('comment/<slug:task_slug>/',
         include([
             path('', comment_task_create, name='comment section'),
             path('<int:pk>/edit/', CommentEditView.as_view(), name='comment edit'),
             path('<int:pk>/delete/', comment_delete_view, name='comment delete'),
         ])),
)
