from django.shortcuts import redirect, get_object_or_404

from forum.main.models import Post, Comment


class RedirectIfNotPostOwner:

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if not post.user == request.user:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class RedirectIfNotCommentOwner:

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=pk)
        if not comment.user == request.user:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)