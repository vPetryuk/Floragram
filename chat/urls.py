from django.urls import path

from . import views
from .views import discussion_list_view, DiscussionDeleteView, DiscussionUpdateView, DiscussionDetailView, \
    add_discussion_view

app_name= 'chat'

urlpatterns = [

    path('', discussion_list_view, name='main-forum-view'),
    path('<pk>/delete/', DiscussionDeleteView.as_view(), name='discussion-delete'),
    path('<pk>/update/', DiscussionUpdateView.as_view(), name='discussion-update'),
    path('<pk>/detail/', DiscussionDetailView.as_view(), name='discussion-detail'),
    path('add-discussion/', add_discussion_view, name='add-discussion-view'),
    path('<str:room_name>/', views.room, name='room'),
]
