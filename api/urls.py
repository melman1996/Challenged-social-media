from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('register/', views.Register.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>', views.PostDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('follow/', views.Follow.as_view()),
    path('followed/', views.FollowedList.as_view()),
    path('followers/', views.FollowerList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)