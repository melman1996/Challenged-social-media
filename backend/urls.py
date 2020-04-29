from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken import views

urlpatterns = [
    path('', include('api.urls')),
    path('api-auth/', views.obtain_auth_token),
]
