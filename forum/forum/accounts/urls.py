from django.urls import path

from forum.accounts.views import LogInView, RegisterView, LogOutView, DeleteProfileView, ProfileView, EditProfileView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
]
