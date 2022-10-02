from django.urls import path, include

from buildin.accounts.views import user_login, user_register, profile_details, profile_edit

urlpatterns = (
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('profile/<int:pk>/',
         include([
             path('', profile_details, name='profile details'),
             path('edit/', profile_edit, name='profile edit'),
                  ]),
))
