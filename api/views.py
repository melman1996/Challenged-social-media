from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.parsers import MultiPartParser, JSONParser
from api.models import *
from api.serializers import *
from api.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User


class PostList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, JSONParser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowedPostList(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        followed = Following.objects.filter(follower=self.request.user)
        followed = [u.followed.id for u in followed]
        return Post.objects.filter(owner__in=followed)


class UserPostList(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        user = User.objects.get(username=username)
        return Post.objects.filter(owner=user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id', None)
        if post_id is None:
            return Comment.objects.all()
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id', None)
        if post_id is None:
            return Like.objects.all()
        return Like.objects.filter(post=post_id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserList(generics.ListAPIView):
    queryset = CustomUserData.objects.all()
    serializer_class = UserDetailSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUserData.objects.all()
    serializer_class = UserDetailSerializer


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    
class FollowedList(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

    def get_queryset(self):
        return Following.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class FollowerList(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

    def get_queryset(self):
        return Following.objects.filter(followed=self.request.user)