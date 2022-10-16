from django.urls import path, include

from buildin.accounts.views import UserLoginView, ProfileDetailsView, profile_edit, UserRegisterView, \
    UserLogoutView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='profile create'),
    path('profile/<int:pk>/',
         include([
             path('', ProfileDetailsView.as_view(), name='profile details'),
             path('edit/', profile_edit, name='profile edit'),
         ]), )

)
