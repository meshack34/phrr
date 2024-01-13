from rest_framework import serializers
from patientapp.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework import serializers
from patientapp.models import *

#Serializers of models

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = "__all__"

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class NursingNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nursing_Notes
        fields = "__all__"

class NursingNotesSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nursing_Notes_sub
        fields = "__all__"

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add any additional data you want to include in the token
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add any additional validation logic or data to include in the response
        return data
