from user.utils.jwt import get_tokens_for_user
from cv001.utils.slugs import Gslug
from user.models import user
from user.utils.utils import is_user
from cv001.messages import *
from .models import *
from rest_framework.views import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class RegisterAsDoctorView(APIView):
    permission_classes = (AllowAny,)
    usermodel = user
    doctormodel = doctor

    def getinsatnce(self, phone):
        instance = self.usermodel.objects.filter(phone_number=phone).first()
        return instance

    def get(self, request):
        try:
            data = request.data.get('otp')
            if data == request.session['otp_instance']:
                phone_number = request.session['phone_number_instance']
                response = {
                    'success': True,
                    'data': {
                        'message': ACCOUNT_CREATED,

                    }
                }
                if not is_user(phone_number):
                    instance = self.usermodel.objects.create(
                        phone_number=phone_number)
                    instance.save()
                    doctorinstance = self.doctormodel.objects.create(
                        UID=instance.UID, slug=Gslug(model=self.doctormodel))
                    token = get_tokens_for_user(instance)
                    response['data']['token'] = token

                else:
                    instance = self.getinsatnce()
                    doctorinstance = self.doctormodel.objects.create(
                        UID=instance.UID, slug=Gslug(model=self.doctormodel))
                    token = get_tokens_for_user(instance)
                    response['data']['token'] = token
                return Response(response, status.HTTP_200_OK)
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


class SpecializationView(APIView):
    permission_classes = (AllowAny,)
    Specializationmodel = specialization

    def post(self, request):
        try:
            data = request.data.get("specialization")
            self.Specializationmodel.objects.create(name=data)
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
