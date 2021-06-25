
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
 path('register/doctor/', RegisterAsDoctorView.as_view(),
         name='doctor regestration'),]