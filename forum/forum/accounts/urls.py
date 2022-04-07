from django.urls import path

from forum.accounts.views import LogInView, RegisterView, LogOutView, DeleteProfileView, ProfileView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]
