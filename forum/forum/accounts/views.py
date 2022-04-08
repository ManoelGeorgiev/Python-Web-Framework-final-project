from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from forum.accounts.forms import LoginForm, RegisterForm, DeleteProfileForm, EditProfileForm
from forum.accounts.mixins import RedirectIfLoggedMixin
from forum.accounts.models import ForumUser, Profile
from forum.common.mixins import RedirectToPreviousMixin
from forum.main.models import Post, Comment


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


class ProfileView(DetailView):
    model = ForumUser
    template_name = 'profile_page.html'
    context_object_name = 'user'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('profile')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number_of_posts'] = Post.objects.filter(closed=False, user=self.object.pk).count()
        context['number_of_comments'] = Comment.objects.filter(post__closed=False, user=self.object.pk).count()
        return context


class EditProfileView(RedirectToPreviousMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = EditProfileForm

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if not pk == request.user.pk:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class DeleteProfileView(LoginRequiredMixin, UpdateView):
    model = ForumUser
    success_url = reverse_lazy('index')
    form_class = DeleteProfileForm
    context_object_name = 'profile'
    template_name = 'delete_profile.html'

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if not pk == request.user.pk:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
