from django.db.models import fields
from doctors.models import doc_specialization, hospital, office, specialization
from rest_framework.serializers import ModelSerializer


class SpecializationSer(ModelSerializer):
    class Meta:
        model = specialization
        fields = ('SPEID', 'name')


class doc_specializationSer(ModelSerializer):
    class Meta:
        model = doc_specialization
        fields = ('SPEID', 'DOCID')


class HospitalSer(ModelSerializer):
    class Meta:
        model = hospital
        fields = '__all__'


class OfficeSer(ModelSerializer):
    class Meta:
        model = office
        fields = '__all__'
