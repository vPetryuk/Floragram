from django.urls import path

from . import views
from .views import discussion_list_view, DiscussionDeleteView, DiscussionUpdateView,add_discussion_view

app_name= 'chat'

urlpatterns = [

    path('', discussion_list_view, name='main-forum-view'),
    path('<pk>/delete/', DiscussionDeleteView.as_view(), name='discussion-delete'),
    path('<pk>/update/', DiscussionUpdateView.as_view(), name='discussion-update'),
    path('add-discussion/', add_discussion_view, name='add-discussion-view'),
    path('<slug:slug>/', views.room, name='room'),
]
