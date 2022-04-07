from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import DeletionMixin
from hitcount.views import HitCountDetailView

from forum.main.forms import CreatePostForm, EditPostForm, DeletePostForm, EditCommentForm, DeleteCommentForm, \
    CreateCommentForm
from forum.main.mixins import RedirectIfNotPostOwnerMixin, RedirectIfNotCommentOwnerMixin, RedirectToPreviousMixin
from forum.main.models import Post, Like, Category, Comment

UserModel = get_user_model()


class HomeView(ListView):
    template_name = 'index.html'
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    ordering = ['-edited_on', '-created_on']

    # prefetch the like and comment sets
    def get_queryset(self):
        queryset = super().get_queryset().filter(closed=False).prefetch_related('like_set', 'comment_set')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = UserModel.objects.all().count()
        context['posts_count'] = Post.objects.filter(closed=False).count()
        context['comments_count'] = Comment.objects.filter(post__closed=False).count()
        try:
            context['latest_user'] = UserModel.objects.latest('date_joined')
        except UserModel.DoesNotExist:
            context['latest_user'] = 'None'
        return context


class CategoryView(ListView):
    template_name = 'category.html'
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    ordering = ['-edited_on', '-created_on']

    # check if category exist before loading the page
    def dispatch(self, request, *args, **kwargs):
        category_pk = self.kwargs['pk']
        category = get_object_or_404(Category, pk=category_pk)
        return super().dispatch(request, *args, **kwargs)

    # prefetch the like and comment sets
    def get_queryset(self):
        queryset = super().get_queryset().filter(closed=False, category_id=self.kwargs['pk']) \
            .prefetch_related('like_set', 'comment_set')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        context['users_count'] = UserModel.objects.all().count()
        context['posts_count'] = Post.objects.filter(closed=False, category_id=self.kwargs['pk']).count()
        try:
            context['latest_user'] = UserModel.objects.latest('date_joined')
        except UserModel.DoesNotExist:
            context['latest_user'] = 'None'
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'create_post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('index')

    # pass the user to the form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditPostView(RedirectIfNotPostOwnerMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = EditPostForm

    def get_success_url(self):
        return reverse_lazy('post details', kwargs={'pk': self.object.pk})


class DeletePostView(RedirectIfNotPostOwnerMixin, LoginRequiredMixin, DeletionMixin, UpdateView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')
    form_class = DeletePostForm


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.pk == post.user_id or not request.user.is_authenticated:
        return redirect('post details', pk)

    new_like, created = Like.objects.get_or_create(user_id=request.user.pk, post_id=pk)
    if not created:
        Like.objects.get(user_id=request.user.pk, post_id=pk).delete()
    return redirect('post details', pk)


class PostDetailsView(HitCountDetailView):
    model = Post
    count_hit = True
    template_name = 'details_post.html'
    context_object_name = 'post'

    # check if the post exists and it's not closed before loading the page
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if post.closed:
            return Http404()
        return super().dispatch(request, *args, **kwargs)

    # prefetch the like and comment sets
    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('like_set', 'comment_set')
        return queryset

    # creates pagination for the comment_set
    def get_related_comments(self):
        queryset = self.object.comment_set.all()
        paginator = Paginator(queryset, 5)
        page = self.request.GET.get('page')
        comments = paginator.get_page(page)
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = self.get_related_comments()
        context['related_comments'] = comments
        context['page_obj'] = comments

        context['is_owner'] = self.object.user == self.request.user
        if self.request.user.is_authenticated:
            context['user_liked'] = self.object.like_set.filter(user=self.request.user) and True or False
        return context


class CreateCommentView(RedirectToPreviousMixin, LoginRequiredMixin, CreateView):
    template_name = 'create_comment.html'
    form_class = CreateCommentForm

    # check if the post exists and it's not closed before loading the page
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if post.closed:
            return Http404()
        return super().dispatch(request, *args, **kwargs)

    # pass the user and post_pk to the form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['post_pk'] = self.kwargs['pk']
        return kwargs

    # def get_success_url(self):
    #     return reverse_lazy('post details', kwargs={'pk': self.kwargs['pk']})


class EditCommentView(RedirectToPreviousMixin, RedirectIfNotCommentOwnerMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'edit_comment.html'
    form_class = EditCommentForm

    # def get_success_url(self):
    #     return reverse_lazy('post details', kwargs={'pk': self.object.post.pk})


class DeleteCommentView(RedirectToPreviousMixin, RedirectIfNotCommentOwnerMixin, LoginRequiredMixin, DeletionMixin, UpdateView):
    model = Comment
    template_name = 'delete_comment.html'
    form_class = DeleteCommentForm

    # def get_success_url(self):
    #     return reverse_lazy('post details', kwargs={'pk': self.object.post.pk})
