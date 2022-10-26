from django.urls import path

from buildin.common.views import HomeView, DashboardView

urlpatterns = (
    path('', HomeView.as_view(), name='home page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
)