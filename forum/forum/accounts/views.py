from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from forum.accounts.forms import LoginForm, RegisterForm, DeleteProfileForm, EditProfileForm
from forum.accounts.mixins import RedirectIfLoggedMixin, RedirectIfNotProfileOwnerMixin
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
        queryset = super().get_queryset().prefetch_related('post_set')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.object.pk).order_by('-created_on')
        context['number_of_comments'] = Comment.objects.filter(user=self.object.pk).count()
        return context


class EditProfileView(RedirectIfNotProfileOwnerMixin, RedirectToPreviousMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = EditProfileForm


class DeleteProfileView(RedirectIfNotProfileOwnerMixin, LoginRequiredMixin, UpdateView):
    model = ForumUser
    success_url = reverse_lazy('index')
    form_class = DeleteProfileForm
    context_object_name = 'profile'
    template_name = 'delete_profile.html'
