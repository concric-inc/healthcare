
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('register/doctor/', RegisterAsDoctorView.as_view(),
         name='doctor regestration'),
    path('doctor/specialization/', SpecializationView.as_view(),
         name='Specialization regestration'),
    path('doctor/specialization/<str:speid>/', SpecializationInstanceView.as_view(),
         name='Specialization regestration instance'),
    path('doctor/specialization/add/<str:speid>/', doc_specializationView.as_view(),
         name='Specialization add'),
    path('doctor/hospital/add/', HospitalView.as_view(),
         name='hospital add'),
]
