from django.urls import path, include

from buildin.accounts.views import UserLoginView, user_register, profile_details, profile_edit, user_logout_view

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/',user_logout_view, name='logout'),
    path('register/', user_register, name='register'),
    path('profile/<int:pk>/',
         include([
             path('', profile_details, name='profile details'),
             path('edit/', profile_edit, name='profile edit'),
                  ]),)

)
