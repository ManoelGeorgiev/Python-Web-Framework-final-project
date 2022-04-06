from django.urls import path

from forum.accounts.views import LogInView, RegisterView, LogOutView, DeleteProfileView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('delete/<int:pk>/', DeleteProfileView.as_view(), name='delete profile')
]