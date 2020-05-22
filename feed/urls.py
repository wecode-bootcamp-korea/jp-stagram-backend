from django.urls import path, include
from feed import views

urlpatterns = [
    path('main', views.FeedView.as_view(), name='feed-main'),
    # path('/post', views.PostView.as_view(), name='feed-post'),
    path('comment', views.CommentView.as_view(), name='feed-comment')
]
