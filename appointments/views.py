from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import views
from .models import Appointment
from .ser import AppointmentSerializer
from rest_framework.response import Response
from rest_framework import status
from cv001.messages import *

class AppointmentView(views.APIView):
    model = Appointment
    ser = AppointmentSerializer

    def post(self, request):
        try:
            data = request.data
            response = {
                'success': False,
                'error': {
                    'message': OTP_INVALID,
                    'code': 409
                }

            }
            return Response(response, status.HTTP_409_CONFLICT, exception=True)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


            
