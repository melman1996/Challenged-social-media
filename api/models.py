from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class CustomUserData(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_data', on_delete=models.CASCADE)
    description = models.TextField(default='')
    avatar = models.ImageField(upload_to='avatars', default=None)


class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    class Meta:
        ordering = ['created']

class Comment(models.Model):
    owner = models.ForeignKey('auth.User', related_name="comments", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

class Following(models.Model):
    follower = models.ForeignKey('auth.User', related_name="follower", on_delete=models.CASCADE)
    followed = models.ForeignKey('auth.User', related_name="followed", on_delete=models.CASCADE)

class Like(models.Model):
    owner = models.ForeignKey('auth.User', related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
