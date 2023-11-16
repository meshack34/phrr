from django.shortcuts import get_object_or_404
from .models import Patient

def get_current_patient(request):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)

    return current_patient
