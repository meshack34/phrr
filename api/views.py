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
from .serializers import (
    AdditionalUserSerializer, DoctorNoteSerializer, LabReportSerializer, PatientSerializer,
    DoctorSerializer, MedicalHistoryySerializer, MedicalHistorySerializer,
    TreatmentRecordSerializer, AccountSerializer, VitalsSerializer,
    HealthcareProfessionalSerializer, HealthcareSpecialtySerializer,
    HealthInsuranceSerializer, PatientAppointmentSerializer,
    CustomTokenObtainPairSerializer,
)

class AdditionalUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AdditionalUserSerializer

    @swagger_auto_schema(responses={200: AdditionalUserSerializer(many=True)})
    def get(self, request, format=None, *args, **kwargs):
        additional_users = AdditionalUser.objects.all()
        serializer = AdditionalUserSerializer(additional_users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=AdditionalUserSerializer)
    def post(self, request, format=None, *args, **kwargs):
        serializer = AdditionalUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Similar views for other models...

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
