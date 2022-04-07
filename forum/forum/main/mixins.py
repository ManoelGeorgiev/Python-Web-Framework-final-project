from django.shortcuts import redirect, get_object_or_404

from forum.main.models import Post, Comment


# throw 404 if the post you are trying to edit/delete doesn't exist
# redirects if not the post owner
class RedirectIfNotPostOwnerMixin:

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if not post.user == request.user:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


# throw 404 if the post for which you are trying to make/edit or delete a comment doesn't exist
# redirects if not the comment owner
class RedirectIfNotCommentOwnerMixin:

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=pk)
        if not comment.user == request.user:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


# try to save the page we are coming from before loading the next page
# and then redirects to it or index if http_referer is off
class RedirectToPreviousMixin:
    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']
