from django.urls import path

from forum.main.views import HomeView, CreatePostView, EditPostView, like_post, PostDetailsView, CategoryView, \
    DeletePostView, EditCommentView, DeleteCommentView, CreateCommentView, like_comment, search_result

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('post/create/', CreatePostView.as_view(), name='create post'),
    path('post/edit/<int:pk>/', EditPostView.as_view(), name='edit post'),
    path('post/details/<int:pk>/', PostDetailsView.as_view(), name='post details'),
    path('post/delete/<int:pk>/', DeletePostView.as_view(), name='delete post'),
    path('post/like/<int:pk>/', like_post, name='like post'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category view'),
    path('post/<int:pk>/comment/', CreateCommentView.as_view(), name='create comment'),
    path('comment/edit/<int:pk>/', EditCommentView.as_view(), name='edit comment'),
    path('comment/delete/<int:pk>/', DeleteCommentView.as_view(), name='delete comment'),
    path('comment/like/<int:pk>/', like_comment, name='like comment'),
    path('search/', search_result, name='search'),
]
