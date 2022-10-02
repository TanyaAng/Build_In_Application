from django.urls import path

from buildin.common.views import home_view

urlpatterns = (
    path('', home_view, name='home page'),
)