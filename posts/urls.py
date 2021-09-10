from django.urls import path

from chat.views import discussion_list_view
from .views import post_comment_create_and_list_view, like_unlike_post, PostDeleteView, PostUpdateView, add_post_view, \
    PostDetailView, recognise_post_view, rec_confirm_post

app_name = 'posts'

urlpatterns = [
    path('', discussion_list_view, name='discussion-list-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
    path('rec-confirm/', rec_confirm_post, name='rec-confirm-post-view'),
    path('<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<pk>/detail/', PostDetailView.as_view(), name='post-detail'),
    path('add-post/', add_post_view, name='add-post-view'),
    path('recognise-post/', recognise_post_view, name='recognise-post-view'),
]
