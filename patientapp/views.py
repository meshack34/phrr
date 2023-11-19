from django.shortcuts import (render, redirect, get_object_or_404,)
from .models import *
from django.shortcuts import render, redirect
from .models import MedicalHistory, TreatmentRecord
from .forms import MedicalHistoryForm, TreatmentRecordForm
from .models import Patient
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .models import Account, Patient
from .models import (
    Patient, MedicalHistoryy, DoctorSpecialization, Medication, Doctor,
    EmergencyContact, MedicalHistoryy, Prescription, PrescriptionStatus,
    AppointmentTime, PatientAppointment, Account, HealthcareProfessional,HealthcareSpecialty,
    HealthInsurance, TreatmentRecord,
)
# views.py
from django.shortcuts import render, redirect
from .models import HealthcareProfessional
from .forms import HealthcareProfessionalForm  # Assuming you have a form for healthcare professionals

from .forms import (
    MedicalTreatmentForm, RegistrationForm, PatientForm,
    EmergencyContactForm, HealthcareExpertForm, HealthcareSpecialityForm,
    HealthInsuranceForm, MedicalHistoryForm, TreatmentRecordForm,
    ExerciseForm, DietaryForm, SmokingForm, AlcoholForm, MedicationsForm,
    LifestyleForm, HealthGoalForm,
)
from django.shortcuts import render, redirect
from .models import MedicalHistory, TreatmentRecord, Patient
from .forms import MedicalHistoryForm, TreatmentRecordForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib import messages, auth
from datetime import date, datetime
from re import split
from .doctorchoices import category, fromTimeChoice, toTimeChoice
from django.contrib.auth.decorators import login_required
from .utils import get_current_patient


def home(request):
    return render(request, 'home/index.html')


def patientregister(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create a user without user_type
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )

            # Set additional fields
            user.phone_number = phone_number
            user.save()

            messages.success(request, 'Registration successful. You can now login.')
            return redirect('login')
                    
    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            current_user = Account.objects.get(id=request.user.id)

            # Assuming that the user type is determined by the presence of a related Patient object
            patient_exists = Patient.objects.filter(user=current_user).exists()

            if patient_exists:
                return redirect('patient_dashboard')
            else:
                # Assuming that the user is not a doctor
                patient = Patient(user=current_user)
                patient.save()
                return redirect('patient_dashboard')
        else:
            messages.success(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'users/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('home')


def patients_profile(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)

    if request.method == 'POST' and current_user.is_authenticated:
        form = PatientForm(request.POST, request.FILES, instance=current_patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.age_years = calculate_age_years(patient.date_of_birth)
            patient.save()  
            return redirect('patient_dashboard')
    else:
        form = PatientForm(instance=current_patient)

    context = {
        'patient': current_patient,
        'form': form,
    }
    return render(request, 'patients/patients-profile.html', context)

def calculate_age_years(date_of_birth):
    today = date.today()
    if date_of_birth:
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
    return None




def manage_emergency_contact(request):
    current_user = request.user
    try:
        current_patient = Patient.objects.get(user=current_user)
    except Patient.DoesNotExist:
        current_patient = None

    if request.method == 'POST' and current_user.is_authenticated:
        form = EmergencyContactForm(request.POST, instance=current_patient.emergency_contact)
        if form.is_valid():
            emergency_contact = form.save(commit=False)
            emergency_contact.user = current_user 
            emergency_contact.save()
            current_patient.emergency_contact = emergency_contact
            current_patient.save()

            return redirect('patient_dashboard')
    else:
        form = EmergencyContactForm(instance=current_patient.emergency_contact)

    context = {
        'form': form,
    }
    return render(request, 'patients/manage_emergency_contact.html', context)


def add_lifestyle_details(request):
    current_patient = get_current_patient(request)

    if request.method == 'POST':
        exercise_form = ExerciseForm(request.POST)
        dietary_form = DietaryForm(request.POST)
        smoking_form = SmokingForm(request.POST)
        alcohol_form = AlcoholForm(request.POST)
        medications_form = MedicationsForm(request.POST)
        lifestyle_form = LifestyleForm(request.POST)

        if all(
            form.is_valid() for form in [exercise_form, dietary_form, smoking_form, alcohol_form, medications_form, lifestyle_form]
        ):
            exercise_form.instance.patient = current_patient
            exercise_form.save()

            dietary_form.instance.patient = current_patient
            dietary_form.save()

            smoking_form.instance.patient = current_patient
            smoking_form.save()

            alcohol_form.instance.patient = current_patient
            alcohol_form.save()

            medications_form.instance.patient = current_patient
            medications_form.save()

            lifestyle_form.instance.patient = current_patient
            lifestyle_form.save()

            return redirect('patient_dashboard')
    else:
        exercise_form = ExerciseForm()
        dietary_form = DietaryForm()
        smoking_form = SmokingForm()
        alcohol_form = AlcoholForm()
        medications_form = MedicationsForm()
        lifestyle_form = LifestyleForm()

    return render(request, 'mm.html', {
        'exercise_form': exercise_form,
        'dietary_form': dietary_form,
        'smoking_form': smoking_form,
        'alcohol_form': alcohol_form,
        'medications_form': medications_form,
        'lifestyle_form': lifestyle_form,
        'current_patient': current_patient
    })


def add_healthcare_professional(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)

        if request.method == 'POST':
            form = HealthcareProfessionalForm(request.POST)
            if form.is_valid():
                professional = form.save(commit=False)
                professional.patient = patient
                professional.save()
                return redirect('healthcare_professionals')
        else:
            form = HealthcareProfessionalForm()

        context = {'form': form}
        return render(request, 'add_healthcare_professional.html', context)
    else:
        # Handle unauthenticated user
        return redirect('login')


# views.py
def healthcare_professionals(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)
        professionals = patient.healthcare_professionals.all()

        context = {'professionals': professionals}
        return render(request, 'healthcare_professionals.html', context)
    else:
        # Handle unauthenticated user
        return redirect('login')


def add_healthcare_speciality(request):
    existing_specialities = HealthcareSpecialty.objects.all()
    if request.method == 'POST':
        form = HealthcareSpecialityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_healthcare_speciality')  
    else:
        form = HealthcareSpecialityForm()
    return render(request, 'add_healthcare_speciality.html', {'form': form, 'existing_specialities': existing_specialities})

# views.py


def add_health_insurance(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)

        if request.method == 'POST':
            form = HealthInsuranceForm(request.POST, request.FILES)
            if form.is_valid():
                insurance = form.save(commit=False)
                insurance.patient = patient
                insurance.save()
                return redirect('health_insurance_list')
        else:
            form = HealthInsuranceForm()

        context = {'form': form}
        return render(request, 'add_health_insurance.html', context)
    else:
        # Handle unauthenticated user
        return redirect('login')
    
def health_insurance_list(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)
        health_insurances = patient.health_insurances.all()

        context = {'health_insurances': health_insurances}
        return render(request, 'health_insurance_list.html', context)
    else:
        # Handle unauthenticated user
        return redirect('login')

# views.py

# views.py


# from django.shortcuts import render, redirect, get_object_or_404
# from .models import MedicalHistory, TreatmentRecord
# from .forms import MedicalHistoryForm, TreatmentRecordForm
# from django.contrib.auth.decorators import login_required

# @login_required
# def add_medical_history(request):
#     if request.method == 'POST':
#         form = MedicalHistoryForm(request.POST)
#         if form.is_valid():
#             medical_history = form.save(commit=False)
#             medical_history.patient = request.user.patient
#             medical_history.save()
#             return redirect('medical_history_list')
#     else:
#         form = MedicalHistoryForm()

#     treatment_form = TreatmentRecordForm()
#     medical_histories = request.user.patient.medical_histories.all()
#     treatment_records = request.user.patient.treatment_records.all()

#     context = {'form': form, 'treatment_form': treatment_form, 'medical_histories': medical_histories, 'treatment_records': treatment_records}
#     return render(request, 'medical_history_and_treatment.html', context)

# @login_required
# def add_treatment_record(request):
#     if request.method == 'POST':
#         form = TreatmentRecordForm(request.POST)
#         if form.is_valid():
#             treatment_record = form.save(commit=False)
#             treatment_record.patient = request.user.patient
#             treatment_record.save()
#             return redirect('medical_history_list')  # Redirect to the medical history list after adding a treatment record
#     else:
#         form = TreatmentRecordForm()

#     medical_history_form = MedicalHistoryForm()
#     medical_histories = request.user.patient.medical_histories.all()
#     treatment_records = request.user.patient.treatment_records.all()

#     context = {'form': form, 'medical_history_form': medical_history_form, 'medical_histories': medical_histories, 'treatment_records': treatment_records}
#     return render(request, 'medical_history_and_treatment.html', context)

# @login_required
# def medical_history_list(request):
#     patient = request.user.patient  # Assuming user is authenticated and has a related Patient
#     medical_histories = patient.medical_histories.all()
#     context = {'medical_histories': medical_histories}
#     return render(request, 'medical_history_list.html', context)


# @login_required
# def medical_history_detail(request, medical_history_id):
#     medical_history = get_object_or_404(MedicalHistory, id=medical_history_id)
#     treatment_records = medical_history.treatment_records.all()

#     context = {'medical_history': medical_history, 'treatment_records': treatment_records}
#     return render(request, 'medical_history_detail.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalHistory, TreatmentRecord, Patient
from .forms import MedicalHistoryyyForm, TreatmentRecordForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalHistory, TreatmentRecord, Patient
from .forms import MedicalHistoryForm, TreatmentRecordForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# @login_required
# def add_medical_history(request):
#     if request.user.is_authenticated:
#         try:
#             patient = request.user.patient  # Try to get the patient associated with the user
#         except Patient.DoesNotExist:
#             return HttpResponse("You need to create a patient profile.")

#         print(request.user)  # Check if the user is printed in the console
#         print(patient)  # Check if the related Patient is printed

#         if request.method == 'POST':
#             form = MedicalHistoryForm(request.POST)
#             if form.is_valid():
#                 medical_history = form.save(commit=False)
#                 medical_history.patient = patient
#                 medical_history.save()
#                 return redirect('medical_history_list')
#         else:
#             form = MedicalHistoryForm()

#         treatment_form = TreatmentRecordForm()
#         medical_histories = patient.medical_histories.all()
#         treatment_records = patient.treatment_records.all()

#         context = {'form': form, 'treatment_form': treatment_form, 'medical_histories': medical_histories, 'treatment_records': treatment_records}
#         return render(request, 'medical_history_and_treatment.html', context)
#     else:
#         # Handle unauthenticated user
#         return redirect('login')


# @login_required
# def add_treatment_record(request):
#     if request.method == 'POST':
#         form = TreatmentRecordForm(request.POST)
#         if form.is_valid():
#             treatment_record = form.save(commit=False)
#             treatment_record.patient = request.user.patient
#             treatment_record.save()
#             return redirect('medical_history_list')  # Redirect to the medical history list after adding a treatment record
#     else:
#         form = TreatmentRecordForm()

#     medical_history_form = MedicalHistoryForm()
#     medical_histories = request.user.patient.medical_histories.all()
#     treatment_records = request.user.patient.treatment_records.all()

#     context = {'form': form, 'medical_history_form': medical_history_form, 'medical_histories': medical_histories, 'treatment_records': treatment_records}
#     return render(request, 'medical_history_and_treatment.html', context)

# @login_required
# def medical_history_list(request):
#     # Ensure that the authenticated user is a patient and has a related patient object
#     if hasattr(request.user, 'patient') and request.user.patient:
#         medical_histories = request.user.patient.medical_histories.all()
#         context = {'medical_histories': medical_histories}
#         return render(request, 'medical_history_list.html', context)
#     else:
#         # Handle the case where the authenticated user is not associated with a patient
#         return redirect('login')  # Or redirect to another appropriate view


def add_medical_history(request):
    if request.method == 'POST':
        medical_history_form = MedicalHistoryyyForm(request.POST)
        treatment_record_form = TreatmentRecordForm(request.POST)

        if medical_history_form.is_valid() and treatment_record_form.is_valid():
            medical_history = medical_history_form.save(commit=False)
            treatment_record = treatment_record_form.save()
            medical_history.save()
            medical_history.treatment_records.add(treatment_record)

            return redirect('medical_history_list') 
    else:
        medical_history_form = MedicalHistoryyyForm()
        treatment_record_form = TreatmentRecordForm()

    return render(request, 'add_medical_history.html', {'medical_history_form': medical_history_form, 'treatment_record_form': treatment_record_form})

def medical_history_detail(request, medical_history_id):
    medical_history = get_object_or_404(MedicalHistory, pk=medical_history_id)
    return render(request, 'medical_history_detail.html', {'medical_history': medical_history})

def medical_history_list(request):
    medical_histories = MedicalHistory.objects.all()
    return render(request, 'medical_history_list.html', {'medical_histories': medical_histories})


def add_health_goal(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)

        if request.method == 'POST':
            form = HealthGoalForm(request.POST)
            if form.is_valid():
                health_goal = form.save(commit=False)
                health_goal.patient = patient
                health_goal.save()
                return redirect('health_goal_list')
        else:
            form = HealthGoalForm()

        context = {'form': form}
        return render(request, 'add_health_goal.html', context)
    else:
        # Handle unauthenticated user
        return redirect('login')

def health_goal_list(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)
        health_goals = patient.health_goals.all()

        context = {'health_goals': health_goals}
        return render(request, 'display_health_goals.html', context)
    else:
        # Handle unauthenticated user
        return redirect('login')


#######################################

def doc_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.user_type = user_type
            user.phone_number = phone_number
            user.save()

            messages.success(request, 'You are now registered and can log in')
            return redirect('login')
                    
    else:
        form = RegistrationForm(request.POST)
    context = {
        'form': form
    }
    return render(request, 'users/doctor-register.html', context)




def doctor_dashboard(request):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor, user=current_user)
    specialization = DoctorSpecialization.objects.filter(doctor=current_doctor)
    
    total_patients = Patient.objects.count()
    # total_patients = Account.objects.filter(user_type='Patient').count()
    today = timezone.now().date()
    patients_registered_today = Account.objects.filter(date_joined__date=today).count()
    print(total_patients)
    patient_appointment = MedicalHistoryy.objects.filter(doctor=current_doctor)
   
    if request.method == 'POST':
        patient_id = request.POST['status']
        accepted_patient = MedicalHistoryy.objects.get(id=patient_id)
        accepted_patient.is_active = True
        accepted_patient.save()
        return redirect('doctor_dashboard')
       
            
    context = {
        'doctor': current_doctor,
        'specialization':specialization,
        'patient_appointment':patient_appointment,
        'total_patients': total_patients,
        'patients_registered_today': patients_registered_today,
        
    }

    return render(request,'users/doctor_dashboard.html', context)

def patient_dashboard(request):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)

    current_appointment = MedicalHistoryy.objects.filter(patient=current_patient) 
    print(current_appointment)
    prescription = Prescription.objects.filter(patient=current_patient)

    prescription_status = PrescriptionStatus.objects.filter(patient=current_patient,is_uploaded=True)
    for status in prescription_status:
        if status.newprescription:
            print(status.newprescription.name)
        else:
            print("Prescription not found for this status.")


    context = {
        'patient': current_patient,
        'current_appointment':current_appointment,
        'prescription':prescription,
        'prescription_status':prescription_status,

    }
    return render(request,'users/patient_dashboard.html', context)


def status(request, patient_id):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor,user=current_user)
    patient = Patient.objects.get(id=patient_id, doctor=current_doctor)


    patientMedicalHistory = MedicalHistoryy.objects.get(patient=patient)
    patientMedicalHistory.is_active = True
    patientMedicalHistory.save()
    return redirect('doctor_dashboard')

def current_patient(request, patient_id):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor,user=current_user)
    patient = Patient.objects.get(id=patient_id)
    doctor_for_patient = MedicalHistoryy.objects.get(patient=patient,doctor=current_doctor)
    accepted_patient = MedicalHistoryy.objects.get(id=patient_id)
    print(accepted_patient)

    prescriptions = PrescriptionStatus.objects.filter(doctor=current_doctor)
    presc_patient = Prescription.objects.filter(patient=patient, doctor=current_doctor)
    context = {
        'current_patient':patient,
        'doctor_for_patient': doctor_for_patient,
        'prescriptions': prescriptions,
        'presc_patient':presc_patient,
        "accepted_patient" :accepted_patient,
    }

    return render(request, 'users/current-patient.html', context)

import io
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from .models import Doctor, Patient, Prescription  # Import your models

@login_required  # Use login_required decorator to ensure the user is authenticated
def getPrescriptionForDoc(request, patient_id):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor, user=current_user)
    patient = get_object_or_404(Patient, id=patient_id)  # Use get_object_or_404 for better error handling

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Use filter() to get a queryset instead of get()
    prescriptions = Prescription.objects.filter(patient=patient, doctor=current_doctor)

    lines = []
    lines.append("Prescription File")
    lines.append(f"Patient: {patient.user.first_name} {patient.user.last_name}")
    lines.append(f"Doctor. :  {current_doctor.user.first_name} {current_doctor.user.last_name}")

    for prescription in prescriptions:
        lines.append(f"Drug Name: {prescription.name}")
        lines.append(f"Quantity: {prescription.quantity}")
        lines.append(f"Days: {prescription.days}")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Set the response content type for PDF
    response = FileResponse(buf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=prescription.pdf'
    return response



def doctor_profile(request):
    current_user = request.user
    current_doctor = Doctor.objects.get(user=current_user)
    specialization = DoctorSpecialization.objects.filter(doctor=current_doctor)
    if request.method == 'POST' and current_user.is_authenticated:
        form = DoctorForm(request.POST, request.FILES, instance=current_doctor)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorForm(instance=current_doctor)
    context = {
        'specialization': specialization,
        'category':category,
        'form':form,
        'doctor':current_doctor,
    }
    return render(request, 'doctors/doctor-profile.html', context)



def getPrescription(request):
    current_user = request.user
    try:
        current_patient = get_object_or_404(Patient, user=current_user)
    except:
        raise ValueError('no patient found')
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    pres = Prescription.objects.filter(patient=current_patient)

    lines = []
    lines.append(" Prescription")
    lines.append("Patient Name: "+current_patient.user.first_name+" "+current_patient.user.last_name)
    for pres in pres:
        lines.append("")
        lines.append("Drug Name: "+pres.name)
        lines.append("Quantity: "+pres.quantity)
        lines.append("Days: "+pres.days)
        
    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='prescriptionfile.pdf')


def show_prescription(request):
    current_user = request.user
    
    current_patient = get_object_or_404(Patient, user=current_user)
    prescription = Prescription.objects.filter(patient=current_patient)
    context = {
        'prescription':prescription,
    }
    return render(request, 'users/patient_dashboard.html', context)



def mypatients(request):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor, user=current_user)
    patient_appointment = MedicalHistoryy.objects.filter(doctor=current_doctor)

    if request.method == 'POST':
        patient_id = request.POST['status']
        accepted_patient = MedicalHistoryy.objects.get(id=patient_id)
        accepted_patient.is_active = True
        accepted_patient.save()
        return redirect('doctor_dashboard')
       
            
    context = {
        'doctor': current_doctor,
        'patient_appointment':patient_appointment,
    }

    return render(request,'doctors/my-patients.html', context)


def doctors(request):
    doctors = Doctor.objects.all()

    context = {
        'doctors':doctors,
    }
    return render(request, 'doctors/doctors.html', context)

def booking(request, doctor_id):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)
    doctor = Doctor.objects.get(id=doctor_id)

    try:
        booked_doctor = MedicalHistoryy.objects.get(doctor=doctor, patient=current_patient)
    except:
        booked_doctor = MedicalHistoryy(doctor=doctor, patient=current_patient)
        booked_doctor.save()
    appoint_time_doctor = AppointmentTime.objects.filter(doctor=doctor)

    appoint_day = appoint_time_doctor.values_list('day',flat=True).distinct()
    appoint_date = appoint_time_doctor.values_list('appointment_date', flat=True)
    time_from = appoint_time_doctor.values_list('time_from',flat=True)
    time_to = appoint_time_doctor.values_list('time_to',flat=True)
    print("from: ", time_from)
    context = {
        'doctor':doctor,
        'appoint_time_doctor' : appoint_time_doctor,
        'appoint_day':appoint_day,
        'time_from': time_from,
        'time_to' : time_to,
        'appoint_date':appoint_date,

    }
    return render(request, 'doctors/booking.html', context)





    

def medical_history(request):

    current_user = request.user
    try:
        current_doctor = get_object_or_404(Doctor, user=current_user)
    except:
        raise ValueError('no doctor found')
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    history = MedicalHistoryy.objects.filter(doctor=current_doctor)

    lines = []

    for hist in history:
        lines.append("")
        lines.append(" ")
        lines.append("      Patient Medical History           ")
        lines.append(" ")
        lines.append("First Name: "+str(hist.first_name))
        lines.append("Last Name: "+str(hist.last_name))
        lines.append("Reason For Visit: "+str(hist.reason))
        lines.append("Weight: "+str(hist.weight))
        lines.append("Gender: "+str(hist.gender))
        lines.append("Previous Operation: "+hist.previous_operation)
        lines.append("Current Medicaion: "+hist.current_medication)
        lines.append("Other Illness: "+hist.other_illness)
        lines.append("Other Information: "+hist.other_information)
        lines.append("       ")
        

    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='medical_history.pdf')

def doctor_specialization(request):
    try:
        current_doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        pass
    if request.method == 'POST':
        category = request.POST.getlist('category')
        for i in range(len(category)):
            specialized_category = DoctorSpecialization( doctor=current_doctor, doctor_category=category[i])
            specialized_category.save()
        return redirect('doctor_profile')


def profile(request, doctor_id):
    current_user = request.user
    # current_patient = get_object_or_404(Patient, user=current_user)
    
    doctor = Doctor.objects.get(id=doctor_id)
    specialization = DoctorSpecialization.objects.get(doctor=doctor)
    appointment = AppointmentTime.objects.filter(doctor=doctor)
    print(appointment)
    context = {
        'doc_profile':doctor,
        'specialization':specialization,
        'appointment':appointment,
        
    }
    return render(request, 'doctors/profile.html', context)


def doctor_search(request):
    doctors = Doctor.objects.order_by('-date_joined') 
    if 'gender_type' in request.GET:
        gender_type = request.GET['gender_type']
        if gender_type:
            doctors = doctors.filter(gender__iexact=gender_type)
            # print("filtered: ",doctors)

    context = {
        'doctors':doctors,
    }
    return render(request, 'doctors/doctor_search.html', context)

def schedule_timing(request, doctor_id):
    current_user = request.user
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":
        time_from = request.POST['time_from']
        time_to = request.POST['time_to']
        appointment_date = request.POST['appointment_date']
        from_to = time_from+"-"+time_to
       
        appointment_date_obj = datetime.datetime.strptime(appointment_date, '%Y-%m-%d')
        day = appointment_date_obj.date().strftime("%A")

        date = appointment_date_obj.date().strftime("%d")
        month = appointment_date_obj.date().strftime("%B")
        print("Date here: ", date)
        print("Month here: ", month)
        print("DDDAAY: ",day)

        appoint_time = AppointmentTime.objects.create(day=day, time_from=time_from, time_to=time_to ,from_to=from_to, date=date, month=month, appointment_date=appointment_date, doctor=doctor)
        appoint_time.save()
        return redirect(request.path_info)

    context = {
        'doctor':doctor,
        'fromTimeChoice': fromTimeChoice,
        'toTimeChoice' : toTimeChoice,
    }

    return render(request, 'doctors/schedule-timing.html',context)



def patient_appointment(request, doctor_id):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":
        from_to = str(request.POST['from_to'])
        print("from_to day:", from_to)
        
        splitted_from_to = from_to.split(',')
        print("Split: ", splitted_from_to[1])

        

        doc_appoint = PatientAppointment(appoint_day=splitted_from_to[1], appoint_time=splitted_from_to[0], doctor=doctor, patient=current_patient)
        doc_appoint.save()



        return redirect('history') 


def appointments(request):
    current_user = request.user
    current_doctor = Doctor.objects.get(user=current_user)

    appointment = MedicalHistoryy.objects.filter(doctor=current_doctor)
    specialization = DoctorSpecialization.objects.filter(doctor=current_doctor)
    context = {
        'current_doctor':current_doctor,
        'appointment':appointment,
        'specialization':specialization,
    }
    return render(request, 'doctors/appointments.html', context)

def viewReview(request):
    current_user = request.user
    current_doctor = Doctor.objects.get(user=current_user)

    context = {
        'doctor':current_doctor,
    }
    return render(request, 'doctors/review.html', context)

def viewReviewOnProfile(request, doctor_id):
    # current_user = request.user
    current_doctor = Doctor.objects.get(id=doctor_id)

    context = {
        'doctor':current_doctor,
    }
    return render(request, 'doctors/profile.html', context)

def deleteAppointment(request, appoint_id):
    appoint_id = MedicalHistoryy.objects.get(id=appoint_id)
    appoint_id.delete()
    return redirect('doctor_dashboard')


def history(request):
    current_user = request.user
    current_patient = get_object_or_404(Patient, user=current_user)

    # Handling MedicalHistoryy form
    if request.method == 'POST':
        try:
            medical_history = MedicalHistoryy.objects.filter(patient=current_patient, is_processing=False).first()
        except MedicalHistoryy.DoesNotExist:
            medical_history = None
        

        medical_form = MedicalHistoryForm(request.POST, instance=medical_history)
        if medical_form.is_valid():
            medical_history = medical_form.save(commit=False)
            medical_history.patient = current_patient
            medical_history.is_processing = True
            medical_history.save()

            return redirect('patient_dashboard')
    else:
        medical_history = MedicalHistoryy.objects.filter(patient=current_patient, is_processing=False).first()
        medical_form = MedicalHistoryForm(instance=medical_history)

    # Handling FamilyMedicalHistory form
    if request.method == 'POST':
        family_form = FamilyMedicalHistoryForm(request.POST)
        if family_form.is_valid():
            family_medical_history = family_form.save(commit=False)
            family_medical_history.patient = current_patient
            family_medical_history.save()

            return redirect('patient_dashboard')
    else:
        family_form = FamilyMedicalHistoryForm()

    # Handling CurrentMedication form
    if request.method == 'POST':
        medication_form = CurrentMedicationForm(request.POST)
        if medication_form.is_valid():
            current_medication = medication_form.save(commit=False)
            current_medication.patient = current_patient
            current_medication.save()

            return redirect('patient_dashboard')
    else:
        medication_form = CurrentMedicationForm()

    # Handling Allergy form
    if request.method == 'POST':
        allergy_form = AllergyForm(request.POST)
        if allergy_form.is_valid():
            allergy = allergy_form.save(commit=False)
            allergy.patient = current_patient
            allergy.save()

            return redirect('patient_dashboard')
    else:
        allergy_form = AllergyForm()

    # Handling Surgery form
    if request.method == 'POST':
        surgery_form = SurgeryForm(request.POST)
        if surgery_form.is_valid():
            surgery = surgery_form.save(commit=False)
            surgery.patient = current_patient
            surgery.save()

            return redirect('patient_dashboard')
    else:
        surgery_form = SurgeryForm()

    # Handling ImmunizationHistory form
    if request.method == 'POST':
        immunization_form = ImmunizationHistoryForm(request.POST)
        if immunization_form.is_valid():
            immunization = immunization_form.save(commit=False)
            immunization.patient = current_patient
            immunization.save()

            return redirect('patient_dashboard')
    else:
        immunization_form = ImmunizationHistoryForm()

    if request.method == 'POST':
        FamilyMedicalHi_form = FamilyMedicalHistoryForm(request.POST)
        if FamilyMedicalHi_form.is_valid():
            familyhistory = FamilyMedicalHi_form.save(commit=False)
            familyhistory.patient = current_patient
            familyhistory.save()

            return redirect('patient_dashboard')
    else:
        FamilyMedicalHi_form = FamilyMedicalHistoryForm()

    context = {
        'medical_form': medical_form,
        'family_form': family_form,
        'medication_form': medication_form,
        'allergy_form': allergy_form,
        'surgery_form': surgery_form,
        'immunization_form': immunization_form,
        'FamilyMedicalHi_form':FamilyMedicalHi_form,
    }
    return render(request, 'documents/medical_history.html', context)




def view_history(request, patient_id):
    # Get the patient object or return a 404 page if not found
    patient = get_object_or_404(Patient, id=patient_id)
    
    medical_history = MedicalHistoryy.objects.filter(patient=patient)
    current_medications = CurrentMedication.objects.filter(patient=patient)
    allergy_data = Allergy.objects.filter(patient=patient)
    surgery_data = Surgery.objects.filter(patient=patient)
    immunization_data = ImmunizationHistory.objects.filter(patient=patient)
    Family_MedicalHistory =FamilyMedicalHistory.objects.filter(patient=patient)
    
    # Create the context dictionary
    context = {
        'patient': patient,
        'medical_history': medical_history,
        'current_medications':current_medications,
        'allergy_data': allergy_data,  
        'surgery_data': surgery_data, 
        'immunization_data': immunization_data,  
        'Family_MedicalHistory': Family_MedicalHistory, 
    }

    return render(request, 'documents/view_history.html', context)


def add_prescription(request, patient_id):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor,user=current_user)
    patient = Patient.objects.get(id=patient_id)
    # print("IDDDDD: ",patient)
    doctor_for_patient = MedicalHistoryy.objects.get(patient=patient,doctor=current_doctor)
    print("Patient ID: ", patient.id)

    speciality = DoctorSpecialization.objects.get(doctor=current_doctor)
    drugName = ''
    quantity = ''
    days = ''
    morning = 'none'
    afternoon = 'none'
    evening='none'
    night='none'

    
    if 'drugName' in request.GET and 'quantity' in request.GET and 'days' in request.GET:
        drugName = request.GET['drugName']
        quantity = request.GET['quantity']
        days = request.GET['days']
        
    if 'morning' in request.GET:
        morning = request.GET['morning']
        # prescription_patient.morning = morning

    if 'afternoon' in request.GET:
        afternoon = request.GET['afternoon']
        # prescription_patient.afternoon = afternoon
    if 'evening' in request.GET:
        evening = request.GET['evening']
        # prescription_patient.evening = evening
    if 'night' in request.GET:
        night = request.GET['night']
        # prescription_patient.night = night

    if drugName != '':
        prescription_patient = Prescription.objects.create(
            patient=patient, 
            doctor=current_doctor,
            name = drugName,
            quantity = quantity,
            days = days,
            morning = morning,
            afternoon = afternoon,
            evening = evening,
            night = night
        )
        prescription_patient.save()
        return redirect(request.path_info)

    prescription = Prescription.objects.filter(doctor=current_doctor, patient=patient)
    context = {
        'current_patient':patient,
        'doctor_for_patient': doctor_for_patient,
        'current_doctor' : current_doctor,
        'speciality':speciality,
        'prescribe_med':prescription,
        # 'form':form,
    }

    return render(request, 'documents/add_prescription.html', context)

# after hitting save button on prescription form
def submitPrescription(request, patient_id):
    current_user = request.user
    current_doctor = get_object_or_404(Doctor,user=current_user)
    patient = Patient.objects.get(id=patient_id)
    if request.method == "POST":
        submit_presc = PrescriptionStatus.objects.create(patient=patient, doctor=current_doctor, is_uploaded=True)
        submit_presc.save()
        return redirect('doctor_dashboard')

def deletePrescItem(request, pres_id):
    print("pres id: ", pres_id)
    presItem = Prescription.objects.get(id=pres_id)
    presItem.delete()
    return redirect(request.META.get('HTTP_REFERER')) #returning previous url/page



def Medication(request, patient_id):
    try:
        current_user = request.user
        patient = get_object_or_404(Patient, id=patient_id)
        current_doctor = get_object_or_404(Doctor, user=current_user)

        # Check if the current doctor has the medical history of the patient
        doctor_for_patient = MedicalHistoryy.objects.get(patient=patient, doctor=current_doctor)
        accepted_patient = MedicalHistoryy.objects.get(id=patient_id)

        speciality = DoctorSpecialization.objects.get(doctor=current_doctor)

        if request.method == 'POST':
            form = MedicalTreatmentForm(request.POST)
            if form.is_valid():
                # Save the form with the current patient and doctor
                medical_history = form.save(commit=False)
                medical_history.patient = patient
                medical_history.doctor = current_doctor
                medical_history.save()
                
                # Handle the many-to-many relationships with selected checkboxes
                form.save_m2m()

                messages.success(request, f'Successfully Added Medical History for {patient}')
                return redirect('home')
        else:
            form = MedicalTreatmentForm(initial={'patient': patient})

        context = {
            'form': form,
            'current_patient': patient,
            'doctor_for_patient': doctor_for_patient,
            'current_doctor': current_doctor,
            'speciality': speciality,
            'accepted_patient': accepted_patient,
        }

        return render(request, 'documents/medical_history_form.html', context)

    except Patient.DoesNotExist:
        # Handle the case where the patient does not exist
        return HttpResponseBadRequest("Patient not found")
    except Doctor.DoesNotExist:
        # Handle the case where the doctor does not exist
        return HttpResponseBadRequest("Doctor not found")

# def Medication(request, patient_id):
#     try:
#         current_user = request.user
#         patient = get_object_or_404(Patient, id=patient_id)
#         current_doctor = get_object_or_404(Doctor, user=current_user)

#         # Check if the current doctor has the medical history of the patient
#         doctor_for_patient = MedicalHistoryy.objects.get(patient=patient, doctor=current_doctor)
#         accepted_patient = MedicalHistoryy.objects.get(id=patient_id)
#         speciality = DoctorSpecialization.objects.get(doctor=current_doctor)

#         if request.method == 'POST':
#             form = MedicalTreatmentForm(request.POST)
#             if form.is_valid():
#                 # Save the form with the current patient and doctor
#                 medical_history = form.save(commit=False)
#                 medical_history.save()
                
#                 # Handle the many-to-many relationships with selected checkboxes
#                 form.save_m2m()

#                 messages.success(request, f'Successfully Added Medical History for {patient}')
#                 return redirect('home')
#         else:
#             form = MedicalTreatmentForm(initial={'patient': patient})

#         context = {
#             'form': form,
#             'current_patient': patient,
#             'doctor_for_patient': doctor_for_patient,
#             'current_doctor': current_doctor,
#             'speciality': speciality,
#             'accepted_patient': accepted_patient,
#         }

#         return render(request, 'documents/medical_history_form.html', context)

#     except Patient.DoesNotExist:
#         # Handle the case where the patient does not exist
#         return HttpResponseBadRequest("Patient not found")
#     except Doctor.DoesNotExist:
#         # Handle the case where the doctor does not exist
#         return HttpResponseBadRequest("Doctor not found")

from django.shortcuts import render, get_object_or_404
from .models import Patient, MedicalHistoryy

from django.shortcuts import render, get_object_or_404
from .models import Patient, Medical_History  # Update the model import

def view_medical_history(request, patient_id):
    # Get the patient object or return a 404 page if not found
    patient = get_object_or_404(Patient, id=patient_id)
    medical_history = Medical_History.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'medical_history': medical_history,
    }

    return render(request, 'documents/view_medical_history.html', context)


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import FileResponse
from .models import Patient, Medical_History  # Update the import for the model

def generate_medical_treatment_pdf(request, patient_id):
    try:
        current_doctor = request.user
        current_doctor = get_object_or_404(Doctor, user=current_doctor)
        
        # Retrieve the patient object
        patient = get_object_or_404(Patient, id=patient_id)

        # Retrieve medical history records for the patient
        medical_history_records = Medical_History.objects.filter(patient=patient)

        # Create a PDF buffer
        buffer = BytesIO()

        # Create a PDF canvas
        c = canvas.Canvas(buffer)

        # Set PDF title and metadata (optional)
        c.setTitle("Medical Treatment Report")
        c.setAuthor("Your Name")
        c.setSubject("Medical Treatment Report for " + patient.user.first_name)

        # Begin adding text to the PDF
        text = c.beginText()
        text.setFont("Helvetica", 12)
        text.setTextOrigin(50, 750)  # Adjust the coordinates as needed

        # Add patient information to the PDF
        text.textLine("Patient: " + patient.user.first_name)
        text.textLine("doctor: " + current_doctor.user.first_name)
        text.textLine("Date: " + str(datetime.date.today()))  # Include date or relevant information

        # Add medical history records to the PDF
        text.textLine("\nMedical Treatment Records:")
        for record in medical_history_records:
            text.textLine("- History: " + record.history)
            text.textLine("- Follow-up Date: " + str(record.follow_up_date))
            text.textLine("- Payment Type: " + record.payment_type.name)
            # text.textLine("- Doctor: " + str(record.doctor.user.first_name()))
            text.textLine("- Total Price: $" + str(record.calculate_total_price()))

            text.textLine("\nReview of Systems:")
            for review in record.review_of_systems.all():
                text.textLine("- " + review.name)

            text.textLine("\nExaminations:")
            for examination in record.examination.all():
                text.textLine("- " + examination.name)

            text.textLine("\nDiagnoses:")
            for diagnosis in record.diagnosis.all():
                text.textLine("- " + diagnosis.name)

            text.textLine("\nTreatments:")
            for treatment in record.treatment.all():
                text.textLine("- " + treatment.name)

            text.textLine("\nInvestigations:")
            for investigation in record.investgation.all():
                text.textLine("- " + investigation.name)

            text.textLine("\nMedications:")
            for medication in record.medication.all():
                text.textLine("- " + medication.name)

        c.drawText(text)

        # Save the PDF
        c.showPage()
        c.save()

        # Reset the buffer position to the beginning
        buffer.seek(0)

        # Create a FileResponse for the PDF download
        response = FileResponse(buffer, as_attachment=True, filename="medical_treatment_report.pdf")

        return response

    except Patient.DoesNotExist:
        return HttpResponseBadRequest("Patient not found")


from django.shortcuts import render, get_object_or_404
from .models import LabReport

def lab_report_confirmation(request, lab_report_id):
    lab_report = get_object_or_404(LabReport, id=lab_report_id)

    context = {
        'lab_report': lab_report,
    }

    return render(request, 'labreport/lab_report_confirmation.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import LabReport, Patient, Doctor, MedicalHistoryy
from .forms import LabReportForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def lab_report(request, patient_id):
    try:
        current_user = request.user
        print(f'Current User: {current_user}')  # Add this line for debugging
        patient = get_object_or_404(Patient, id=patient_id)
        print(f'Patient: {patient}')  # Add this line for debugging
        current_doctor = get_object_or_404(Doctor, user=current_user)
        print(f'Current Doctor: {current_doctor}')  # Add this line for debugging

        # Check if the current doctor has the medical history of the patient
        doctor_for_patient = MedicalHistoryy.objects.get(patient=patient, doctor=current_doctor)

        if request.method == 'POST':
            form = LabReportForm(request.POST)
            if form.is_valid():
                lab_report = form.save(commit=False)
                lab_report.patient = patient
                lab_report.doctor = current_doctor
                lab_report.save()
            
                confirmation_url = reverse('lab_report_confirmation', args=[lab_report.id])
                return HttpResponseRedirect(confirmation_url)
        else:
            form = LabReportForm()

        context = {
            'form': form,
            'current_patient': patient,
            'doctor_for_patient': doctor_for_patient,
            'current_doctor': current_doctor,
        }

        return render(request, 'labreport/create_lab_report.html', context)

    except Patient.DoesNotExist:
        return HttpResponseBadRequest("Patient not found")
    except Doctor.DoesNotExist:
        return HttpResponseBadRequest("Doctor not found")

