from django.shortcuts import render
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from patientapp.models import (
    AdditionalUser, DoctorNote, LabReport, Patient, Doctor, MedicalHistoryy,
    MedicalHistory, TreatmentRecord, Account, Vitals, HealthcareProfessional,
    HealthcareSpecialty, HealthInsurance, PatientAppointment,
)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'username', 'phone_number']

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

from .serializers import (
    AccountSerializer, RegistrationSerializer, EmergencyContactSerializer, CustomTokenObtainPairSerializer,
)

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HomeView(APIView):
    def get(self, request, format=None):
        return Response(data={'message': 'Welcome to the API!'}, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from rest_framework import serializers
from patientapp.views import *

class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    security_question_1 = serializers.CharField()
    security_answer_1 = serializers.CharField()
    security_question_2 = serializers.CharField()
    security_answer_2 = serializers.CharField()

    def create(self, validated_data):
        # Generate account_id
        account_id = generate_account_id()

        # Create a user with the account_id
        user = Account.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password'],
            account_id=account_id,
            security_question_1=validated_data['security_question_1'],
            security_answer_1=validated_data['security_answer_1'],
            security_question_2=validated_data['security_question_2'],
            security_answer_2=validated_data['security_answer_2'],
        )

        # Set additional fields
        user.phone_number = validated_data['phone_number']
        user.save()

        # Send SMS verification
        sms_response = send_sms_verification(validated_data['phone_number'], account_id)
        print('sms_response', sms_response)

        # Send Email verification
        email_response = send_email_verification(validated_data['email'], account_id)
        print('email_response', email_response)

        return user




# Similar views for other models...

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
