from rest_framework import serializers
from api.models import *
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Post
        fields = ['id', 'owner', 'description', 'image', 'created']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Comment
        fields = ['id', 'owner', 'content', 'post']


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Like
        fields = ['id', 'owner', 'post']


class UserDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = CustomUserData
        fields = ['id', 'username', 'description', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
            username = self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.save()
        user_detail = CustomUserData(
            user = user,
            description = '',
            avatar = None
        )
        user_detail.save()
        return user


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = ['followed', 'follower']