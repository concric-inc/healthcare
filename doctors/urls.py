from user.models import PhoneNumber
from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('/')
]