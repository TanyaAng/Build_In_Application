from django.urls import path

from buildin.common.views import HomeView

urlpatterns = (
    path('', HomeView.as_view(), name='home page'),
)