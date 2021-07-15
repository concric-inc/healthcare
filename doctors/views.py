from doctors.utils.modelfunctions import doctorinsatnce, getDocId
from cv001.utils.utils import get_JWT_token, get_uid
from doctors.ser import HospitalSer, SpecializationSer, doc_specializationSer
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

    def is_doctor(self, phone_number):
        instance = self.usermodel.objects.filter(
            phone_number=phone_number).first()
        return self.doctormodel.objects.filter(UID=instance.UID).exists()

    def getinsatnce(self, phone):
        instance = self.usermodel.objects.filter(phone_number=phone).first()
        return instance

    def post(self, request):
        try:
            data = request.data.get('otp')
            if data == request.session['otp_instance']:
                del request.session['otp_instance']
                phone_number = request.session['phone_number_instance']
                if self.is_doctor(phone_number=phone_number):
                    response = {
                        'success': False,
                        'error': {
                            'message': USER_ALREADY_EXISTS,
                            'code': 409
                        }

                    }
                    return Response(response, status.HTTP_409_CONFLICT, exception=True)

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
                    doctorinstance.save()
                    token = get_tokens_for_user(instance)
                    response['data']['token'] = token

                else:
                    instance = self.getinsatnce(phone_number)
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
    ser = SpecializationSer

    def post(self, request):
        try:
            data = request.data.get("specialization")
            Specializationinstance = self.Specializationmodel.objects.create(
                name=data)
            Specializationinstance.save()
            response = {
                'success': True,
                'data': {
                    'message': SPECIALIZATION_ADDED,
                }
            }
            return Response(response, status.HTTP_200_OK)
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

    def get(self, request):
        try:
            Specializationinstance = self.Specializationmodel.objects.all()
            serinstance = self.ser(Specializationinstance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
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


class SpecializationInstanceView(APIView):
    permission_classes = (AllowAny,)
    Specializationmodel = specialization
    ser = SpecializationSer

    def getinsatnce(self, id):
        instance = self.Specializationmodel.objects.filter(SPEID=id).first()
        if instance:
            print("hello")
            return instance
        else:
            raise NotFound(detail='specialization not found',
                           code=status.HTTP_404_NOT_FOUND)

    def get(self, request, speid):
        try:
            Specializationinstance = self.getinsatnce(speid)
            serinstance = self.ser(Specializationinstance)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }

            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, speid):
        try:
            instance = self.getinsatnce(speid)
            instance.delete()
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }

            return Response(response, status=status.HTTP_404_NOT_FOUND)


class doc_specializationView(APIView):
    ser = doc_specializationSer
    model = doc_specialization

    def getinsatnce(self, id):
        instance = self.model.objects.filter(SPEID=id).all()
        if instance:
            return instance
        else:
            raise NotFound(detail='not found',
                           code=status.HTTP_404_NOT_FOUND)

    def post(self, request, speid):
        try:

            doc_instance_doci = getDocId(request=request)
            instance = self.model.objects.create(
                SPEID=speid, DOCID=doc_instance_doci)
            instance.save()
            response = {
                'success': True,
                'data': {
                    'message': SPECIALIZATION_ADDED,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status.HTTP_404_NOT_FOUND)

    def get(self, request, speid):
        """
        for getting all doctors related to a specilazation
        """
        try:
            instance = self.getinsatnce(speid)
            serinstance = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class HospitalView(APIView):
    model = hospital
    ser = HospitalSer

    def getinsatnce(self, id):
        instance = self.model.objects.filter(DOCID=id).all()
        if instance:
            return instance
        else:
            raise NotFound(detail='hospital not found',
                           code=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            docid = getDocId(request=request)
            data = request.data
            instance = self.model.objects.create(
                DOCID=docid, name=data['hospital_name'], city=data['hospital_city'],
                start=data['start'], end=data['end'])
            instance.save()
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            docid = getDocId(request=request)
            instance = self.getinsatnce(docid)
            serdata = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serdata.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class OfficeView(APIView):
    model = office

    def post(self, request):
        try:
            docid = getDocId(request=request)
            data = request.data
            instance = self.model.objects.create(
                DOCID=docid, min_time_slot=data['min_time_slot'], first_consultation_fee=data['first_consultation_fee'], follow_up_fee=data['follow_up_fee'])
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            docid = getDocId(request=request)
            
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
