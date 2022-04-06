from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from forum.accounts.forms import LoginForm, RegisterForm, DeleteProfileForm
from forum.accounts.mixins import RedirectIfLoggedMixin
from forum.accounts.models import ForumUser


class LogInView(RedirectIfLoggedMixin, LoginView):
    template_name = 'login_page.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().success_url


class LogOutView(LogoutView):
    next_page = reverse_lazy('index')


class RegisterView(RedirectIfLoggedMixin, CreateView):
    form_class = RegisterForm
    template_name = 'register_page.html'
    success_url = reverse_lazy('index')


class DeleteProfileView(UpdateView):
    model = ForumUser
    success_url = reverse_lazy('index')
    form_class = DeleteProfileForm
    context_object_name = 'profile'
    template_name = 'delete_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == self.kwargs['pk']:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
