from django.utils.http import urlsafe_base64_decode
from django.template.loader import get_template
from .forms import PatientDischargeForm
from django.shortcuts import render
from django.http import Http404
from .models import AdditionalUser
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .forms import DoctorNoteForm
from .models import AdditionalUser, DoctorNote
from django.http import HttpResponse, HttpResponseServerError
from xhtml2pdf import pisa
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import LabReport, Patient, Doctor, MedicalHistoryy
from .forms import LabReportForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import MedicalHistory, TreatmentRecord
from .forms import MedicalHistoryForm, TreatmentRecordForm
from django.urls import path
from django.views.generic.edit import CreateView
from .forms import AdditionalUserForm
from django.contrib.auth import authenticate, login as auth_login
from .models import Account
from .forms import VitalsForm
from .models import Vitals
from django.contrib import messages
from .forms import NEWMedicalHistoryForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalHistory, TreatmentRecord, Patient
from .forms import MedicalHistoryyyForm, TreatmentRecordForm
from django.contrib.auth.decorators import login_required
from .models import AdditionalUser
from .models import LabReport
from .models import HealthcareProfessional
from .forms import HealthcareProfessionalForm
from .models import MedicalHistory, TreatmentRecord
from .forms import MedicalHistoryForm, TreatmentRecordForm


from .models import (
    Patient, MedicalHistoryy, DoctorSpecialization, Medication, Doctor,
    EmergencyContact, MedicalHistoryy, Prescription, PrescriptionStatus,NewmedicalHistory,
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


import random
import string
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from .models import Account, Patient
from phonenumbers import parse as parse_phone_number, PhoneNumberFormat
from twilio.rest import Client
import os
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from .models import Account, Patient
import random
import string
from phonenumbers import parse as parse_phone_number, PhoneNumberFormat
from twilio.rest import Client
import os
from django.core.mail import send_mail
from .forms import RegistrationForm
from .models import Account
from twilio.rest import Client
import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
import random
import string
from .models import Account

import random
import string
from django.db.models import Max
from .models import Account  # Assuming your Account model is in a file named models.py

def generate_account_id():
    length = 8 
    while True:
        first_chars = "Acc" + ''.join(random.choices(string.ascii_letters, k=length - 4))
        last_digits = str(random.randint(0, 999)).zfill(3)
        account_id = first_chars + last_digits
        if not Account.objects.filter(account_id=account_id).exists():
            break

    return account_id


def send_sms_verification(phone_number, account_id):
    account_sid = "AC3bac06f325e90b66ced3c2b641b08f7a"
    auth_token = "595e740fbc4b1fe7ab163ec10d4fa5db"
    client = Client(account_sid, auth_token)
    twilio_phone_number = "+15108582603"
    message = client.messages.create(
        body=f"Your account ID is {account_id}",
        from_=twilio_phone_number,
        to=phone_number
    )
    return message.sid

def send_email_verification(email, account_id):
    subject = 'Your Account ID'
    message = f'Your account ID is {account_id}.'
    from_email = 'meshackkimutai34@gmail.com'  
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    

def patient_register(request):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                security_question_1 = form.cleaned_data['security_question_1']
                security_answer_1 = form.cleaned_data['security_answer_1']
                security_question_2 = form.cleaned_data['security_question_2']
                security_answer_2 = form.cleaned_data['security_answer_2']

                # Generate account_id
                account_id = generate_account_id()
                
                # Create a user with the account_id
                user = Account.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=email,
                    password=password,
                    account_id=account_id,
                    security_question_1=security_question_1,
                    security_answer_1=security_answer_1,
                    security_question_2=security_question_2,
                    security_answer_2=security_answer_2,
                )

                # Set additional fields
                user.phone_number = phone_number
                user.save()

                # Send SMS verification
                sms_respose=send_sms_verification(phone_number, account_id)
                print('sms_respose',sms_respose)

                # Send Email verification
                email_respose=send_email_verification(email, account_id)
                print('email_respose',email_respose)

                messages.success(request, 'Registration successful. Check your phone and email for the account ID.')
                return redirect('login')
                        
        else:
            form = RegistrationForm()
        
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)


def user_login(request):
    if request.method == 'POST':
        account_id = request.POST['account_id']
        password = request.POST['password']

        user = authenticate(request, account_id=account_id, password=password)

        if user is not None:
            auth_login(request, user)
            current_user = Account.objects.get(id=request.user.id)
            patient_exists = Patient.objects.filter(user=current_user).exists()

            if patient_exists:
                return redirect('patient_dashboard')
            else:
                patient = Patient(user=current_user)
                patient.save()
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'users/login.html')




def recover_account_id(request):
    if request.method == 'POST':
        # Extract data from the form
        security_question_1 = request.POST.get('security_question_1')
        security_answer_1 = request.POST.get('security_answer_1')
        security_question_2 = request.POST.get('security_question_2')
        security_answer_2 = request.POST.get('security_answer_2')
        account = Account.objects.get_account_by_security_answers(
            security_question_1=security_question_1,
            security_answer_1=security_answer_1,
            security_question_2=security_question_2,
            security_answer_2=security_answer_2,
        )
        if account:
            return render(request, 'users/account_recovery_result.html', {'account_id': account.account_id})
        else:
            # Account not found or security answers are incorrect
            return render(request, 'users/account_recovery.html', {'error_message': 'Invalid security answers'})
    else:
        # Display the form to input security answers
        return render(request, 'users/account_recovery.html')

def discharge_form(request):
    if request.method == 'POST':
        form = PatientDischargeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form = PatientDischargeForm()

    return render(request, 'discharge_form_pdf.html', {'form': form})

# views.p


def account_recovery(request):
    if request.method == 'POST':
        security_answer_1 = request.POST.get('security_answer_1')
        security_answer_2 = request.POST.get('security_answer_2')

        user = Account.objects.filter(
            security_answer_1=security_answer_1,
            security_answer_2=security_answer_2
        ).first()

        if user:
            # Retrieve the existing account ID
            account_id = user.account_id

            # Send recovery details via email and SMS
            send_email_verification(user.email, account_id)
            send_sms_verification(user.phone_number, account_id)

            messages.success(request, 'Recovery details sent to your email and phone number.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid security answers. Please try again.')

    return render(request, 'users/account_recoveryy.html')

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


def send_password_reset_email(email, token):
    subject = 'Reset Your Password'
    message = f'Click the link to reset your password: {settings.BASE_URL}/reset_password/{urlsafe_base64_encode(force_bytes(email))}/{token}/'
    from_email = 'meshackkimutai34@gmail.com'  
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = Account.objects.filter(email=email).first()

        if user:
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            user.password_reset_token = token
            user.password_reset_token_created_at = timezone.now()
            user.save()

            # Send password reset details via email
            send_password_reset_email(user.email, user.password_reset_token)

            messages.success(request, 'Password reset details sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid email address. Please try again.')

    return render(request, 'users/forgot_password.html')




def reset_password(request, email_b64, token):
    try:
        email = urlsafe_base64_decode(email_b64).decode('utf-8')
        user = Account.objects.get(email=email, password_reset_token=token)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        # Invalid token or email
        messages.error(request, 'Invalid password reset link.')
        return redirect('login')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            # Set the new password and clear the token
            user.set_password(new_password)
            user.password_reset_token = None
            user.password_reset_token_created_at = None
            user.save()

            messages.success(request, 'Password reset successful. You can now log in with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'users/reset_password.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import AdditionalUserForm
from .models import AdditionalUser, Account

from .forms import AdditionalUserForm
from .forms import AdditionalUserForm

# @login_required(login_url='login')
# def create_additional_user(request):
#     current_user = request.user

#     if request.method == 'POST' and current_user.is_authenticated:
#         form = AdditionalUserForm(request.POST, request.FILES)  # Include request.FILES
#         if form.is_valid():
#             additional_user = form.save(commit=False)
            
#             # Use create_user method to handle password hashing
#             additional_account = Account.objects.create_user(
#                 email=additional_user.email,
#                 username=additional_user.username,
#                 password=additional_user.password,  # Include password for Account
#                 account_id=generate_account_id(),
#                 first_name=additional_user.first_name,
#                 last_name=additional_user.last_name,
#                 phone_number=additional_user.phone_number,
#                 security_question_1=additional_user.security_question_1,
#                 security_answer_1=additional_user.security_answer_1,
#                 security_question_2=additional_user.security_question_2,
#                 security_answer_2=additional_user.security_answer_2,
#             )
#             additional_user.password = None
#             additional_user.account = additional_account
#             additional_user.creator = current_user
#             additional_user.save()
            
#             return redirect('patient_dashboard')  # Replace 'home' with the URL name of your home page
#     else:
#         form = AdditionalUserForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'users/create_additional_user.html', context)

@login_required(login_url='login')
def create_additional_user(request):
    current_user = request.user

    if request.method == 'POST' and current_user.is_authenticated:
        form = AdditionalUserForm(request.POST, request.FILES)

        if form.is_valid():
            additional_user = form.save(commit=False)

            additional_account = Account.objects.create_user(
                email=additional_user.email,
                username=additional_user.username,
                account_id=generate_account_id(),
                first_name=additional_user.first_name,
                last_name=additional_user.last_name,
                phone_number=additional_user.phone_number,
                security_question_1=additional_user.security_question_1,
                security_answer_1=additional_user.security_answer_1,
                security_question_2=additional_user.security_question_2,
                security_answer_2=additional_user.security_answer_2,
            )

            
            additional_user.account = additional_account
            additional_user.creator = current_user
            additional_user.save()

            # Redirect to the appropriate page after successful creation
            return redirect('patient_dashboard')  # Replace with the URL name of your destination page

    else:
        form = AdditionalUserForm()

    context = {
        'form': form,
    }

    return render(request, 'users/create_additional_user.html', context)


def display_additional_users(request):
    current_user = request.user
    active_additional_users = AdditionalUser.objects.filter(creator=current_user, is_active=True)
    inactive_additional_users = AdditionalUser.objects.filter(creator=current_user, is_active=False)

    context = {
        'active_additional_users': active_additional_users,
        'inactive_additional_users': inactive_additional_users,
    }
    return render(request, 'users/patient_dashboard.html', context)


from django.shortcuts import get_object_or_404

def user_details(request, additional_user_id):
    try:
        # Convert additional_user_id to an integer
        additional_user_id = int(additional_user_id)
        
        user = get_object_or_404(AdditionalUser, additional_user_id=additional_user_id)
    except ValueError:
        raise Http404("Invalid additional_user_id")
    
    return render(request, 'users/user_details.html', {'user': user})

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import AdditionalUser

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import AdditionalUser

def download_file(request, additional_user_id, file_type):
    additional_user = get_object_or_404(AdditionalUser, additional_user_id=additional_user_id)

    # Determine the file field based on file_type
    if file_type == 'referralnotes':
        file_field = 'referralnotes'
    elif file_type == 'doctors_notes':
        file_field = 'doctors_notes'
    elif file_type == 'preproceduralnotes':
        file_field = 'preproceduralnotes'
    else:
        raise Http404("Invalid file_type")

    file_instance = getattr(additional_user, file_field)

    if file_instance:
        file_path = file_instance.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={file_instance.name}'
            return response

    return HttpResponse("File not found")

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import AdditionalUser
from django.shortcuts import render, redirect, get_object_or_404
from .models import AdditionalUser

# def upload_file(request, additional_user_id, file_type):
#     user = get_object_or_404(AdditionalUser, additional_user_id=additional_user_id)

#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('patient_dashboard')  # Redirect to a success page
#     else:
#         form = FileUploadForm(instance=user)

#     return render(request, 'users/user_details.html', {'user': user, 'form': form})

# views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import AdditionalUser, FileUpload
# from .forms import FileUploadForm

# def upload_file(request, user_id, file_type):
#     user = get_object_or_404(AdditionalUser, additional_user_id=user_id)

#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_upload = form.save(commit=False)
#             file_upload.user = user
#             file_upload.save()
#             return redirect('patient_dashboard')  # Redirect to a success page
#     else:
#         form = FileUploadForm()

#     file_uploads = FileUpload.objects.filter(user=user)

#     return render(request, 'users/user_details.html', {'user': user, 'form': form, 'file_uploads': file_uploads})#


#views

# views.py
from django.shortcuts import render, redirect
from .models import AdditionalUser, FileUpload
from .forms import FileUploadForm
# views.py
from django.shortcuts import render, redirect
from .models import AdditionalUser, FileUpload
from .forms import FileUploadForm

def upload_file(request, additional_user_id):
    additional_user = AdditionalUser.objects.get(pk=additional_user_id)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_upload = form.save(commit=False)
            file_upload.user = additional_user
            file_upload.save()
            return redirect('upload_file', additional_user_id=additional_user_id)
    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form, 'additional_user': additional_user})


from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

def view_file(request, file_upload_id):
    file_upload = get_object_or_404(FileUpload, pk=file_upload_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_upload.file.name)
    
    with open(file_path, 'rb') as file:
        response = FileResponse(file)
        return response






# def upload_file(request, additional_user_id, file_type):
#     additional_user = get_object_or_404(AdditionalUser, additional_user_id=additional_user_id)

#     # Determine the file field based on file_type
#     if file_type == 'referralnotes':
#         file_field = 'referralnotes'
#     elif file_type == 'doctors_notes':
#         file_field = 'doctors_notes'
#     elif file_type == 'preproceduralnotes':
#         file_field = 'preproceduralnotes'
#     else:
#         raise Http404("Invalid file_type")

#     if request.method == 'POST' and request.FILES.get('file'):
#         uploaded_file = request.FILES['file']
#         setattr(additional_user, file_field, uploaded_file)
#         additional_user.save()

#         # Redirect to the home page or another desired URL
#         return redirect('patient_dashboard')

#     return render(request, 'file/upload_file.html', {'additional_user': additional_user})


def toggle_active(request, additional_user_id):
    additional_user = get_object_or_404(AdditionalUser, additional_user_id=additional_user_id)
    additional_user.is_active = not additional_user.is_active
    additional_user.save()
    return redirect('patient_dashboard') 

@login_required(login_url='login')
def patient_dashboard(request):
    current_user = request.user
    active_additional_users = AdditionalUser.objects.filter(creator=current_user, is_active=True)
    inactive_additional_users = AdditionalUser.objects.filter(creator=current_user, is_active=False)

    context = {
        'active_additional_users': active_additional_users,
        'inactive_additional_users': inactive_additional_users,
    }
    return render(request, 'users/patient_dashboard.html', context)



def doctor_note_form(request, additional_user_id):
    try:
        additional_user_id = int(additional_user_id)
        user = get_object_or_404(AdditionalUser, additional_user_id=additional_user_id)

        if request.method == 'POST':
            form = DoctorNoteForm(request.POST)
            if form.is_valid():
                doctor_note = form.save(commit=False)
                doctor_note.additional_user = user
                doctor_note.save()
                return redirect('patient_dashboard')

        else:
            form = DoctorNoteForm()

        context = {
            'form': form,
            'user': user,
        }
        return render(request, 'users/doctor_note_form.html', context)

    except ValueError:
        return render(request, 'users/invalid_user_id.html')


def view_nursing_notes(request, additional_user_id):
    try:
        additional_user_id = int(additional_user_id)
        user = get_object_or_404(AdditionalUser, additional_user_id=additional_user_id)

        if request.method == 'POST':
            form = DoctorNoteForm(request.POST)
            if form.is_valid():
                doctor_note = form.save(commit=False)
                doctor_note.additional_user = user
                doctor_note.save()
                return redirect('patient_dashboard')

        else:
            form = DoctorNoteForm()

        context = {
            'form': form,
            'user': user,
        }
        return render(request, 'neww.html', context)

    except ValueError:
        return render(request, 'users/invalid_user_id.html')




def render_to_pdf(template_path, context):
    template_str = render_to_string(template_path, context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    pisa_status = pisa.CreatePDF(template_str, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + template_str + '</pre>')
    return response





@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='login')
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


@login_required(login_url='login')
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

#Health speciality
@login_required(login_url='login')
def add_healthcare_speciality(request):
    existing_specialities = HealthcareSpecialty.objects.all()
    if request.method == 'POST':
        form = HealthcareSpecialityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_healthcare_speciality')  
    else:
        form = HealthcareSpecialityForm()
    return render(request, 'speciality/add_healthcare_speciality.html', {'form': form, 'existing_specialities': existing_specialities})
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def update_healthcare_speciality(request, pk):
    healthcare_specialty = get_object_or_404(HealthcareSpecialty, pk=pk)
    existing_specialities = HealthcareSpecialty.objects.all()

    if request.method == 'POST':
        form = HealthcareSpecialityForm(request.POST, instance=healthcare_specialty)
        if form.is_valid():
            form.save()
            return redirect('add_healthcare_speciality')  
    else:
        form = HealthcareSpecialityForm(instance=healthcare_specialty)

    return render(request, 'speciality/update_healthcare_speciality.html', {'form': form, 'speciality': healthcare_specialty, 'existing_specialities': existing_specialities})


@login_required(login_url='login')
def delete_healthcare_speciality(request, pk):
    healthcare_specialty = get_object_or_404(HealthcareSpecialty, pk=pk)

    if request.method == 'POST':
        healthcare_specialty.delete()
        return redirect('add_healthcare_speciality')

    return render(request, 'speciality/delete_healthcare_speciality.html', {'healthcare_specialty': healthcare_specialty})

######## end specilization
########


@login_required(login_url='login')
def add_healthcare_professional(request):
    current_user = request.user
    if request.method == 'POST':
        form = HealthcareProfessionalForm(request.POST)
        if form.is_valid():
            healthcare_professional = form.save(commit=False)
            
            try:
                # Attempt to get the patient associated with the current user
                patient = Patient.objects.get(user=current_user)
                healthcare_professional.patient = patient
                healthcare_professional.save()
                messages.success(request, 'Healthcare professional added successfully.')
                return redirect('healthcare_professionals')
            
            except Patient.DoesNotExist:
                # Handle the case where the patient is not found for the current user
                messages.error(request, 'Patient not found. Please make sure your account is associated with a patient.')
                return redirect('add_healthcare_professional')

    else:
        form = HealthcareProfessionalForm()

    return render(request, 'speciality/add_healthcare_professional.html', {'form': form})


# views.py
@login_required(login_url='login')
def healthcare_professionals(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)
        professionals = patient.healthcare_professionals.all()

        context = {'professionals': professionals}
        return render(request, 'speciality/healthcare_professionals.html', context)
    else:
        return redirect('login')

################################end health care professional
# views.py

@login_required(login_url='login')
def add_health_insurance(request):
    current_user = request.user
    try:
        # Attempt to get the patient associated with the current user
        patient = Patient.objects.get(user=current_user)
        
        if request.method == 'POST':
            form = HealthInsuranceForm(request.POST, request.FILES)
            if form.is_valid():
                health_insurance = form.save(commit=False)
                health_insurance.patient = patient
                health_insurance.save()
                messages.success(request, 'Health insurance information added successfully.')
                return redirect('health_insurance_list')

        else:
            form = HealthInsuranceForm()

        return render(request, 'add_health_insurance.html', {'form': form})
    
    except Patient.DoesNotExist:
        # Handle the case where the patient is not found for the current user
        messages.error(request, 'Patient not found. Please make sure your account is associated with a patient.')
        return redirect('add_health_insurance')

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HealthInsurance
from .forms import HealthInsuranceForm
from .models import Patient

@login_required(login_url='login')
def view_health_insurance(request):
    current_user = request.user

    try:
        # Attempt to get the patient associated with the current user
        patient = Patient.objects.get(user=current_user)

        # Use filter() to get a queryset of health insurances associated with the patient
        health_insurances = HealthInsurance.objects.filter(patient=patient)

        # Check if any health insurances were found
        if health_insurances.exists():
            # Use the first health insurance entry (you might want to implement logic to handle multiple entries)
            health_insurance = health_insurances.first()

            return render(request, 'healthinsurance/health_insurance_list.html.html', {'health_insurance': health_insurance})
        
        else:
            # Handle the case where no health insurance entry is found
            messages.error(request, 'No health insurance information found.')
            return redirect('add_health_insurance')

    except Patient.DoesNotExist:
        # Handle the case where the patient is not found for the current user
        messages.error(request, 'Patient not found. Please make sure your account is associated with a patient.')
        return redirect('add_health_insurance')


    
def health_insurance_list(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)
        health_insurances = patient.health_insurances.all()

        context = {'health_insurances': health_insurances}
        return render(request, 'health_insurance_list.html', context)
    else:
        # Handle unauthenticated user
        return redirect('login')



#########################add vitals
@login_required(login_url='login')
def add_vitals(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)

    if request.method == 'POST':
        form = VitalsForm(request.POST)
        if form.is_valid():
            vitals = form.save(commit=False)
            vitals.patient = current_patient
            vitals.save()
            messages.success(request, 'Vitals recorded successfully.')
            return redirect('view_vitals')
    else:
        form = VitalsForm()

    context = {
        'form': form,
    }
    return render(request, 'vitals/add_vitals.html', context)

@login_required(login_url='login')
def view_vitals(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    vitals_records = Vitals.objects.filter(patient=current_patient)

    context = {
        'vitals_records': vitals_records,
    }
    return render(request, 'vitals/view_vitals.html', context)

@login_required(login_url='login')
def update_vitals(request, vitals_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    vitals_instance = get_object_or_404(Vitals, id=vitals_id, patient=current_patient)

    if request.method == 'POST':
        form = VitalsForm(request.POST, instance=vitals_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vitals updated successfully.')
            return redirect('view_vitals')
    else:
        form = VitalsForm(instance=vitals_instance)

    context = {
        'form': form,
    }
    return render(request, 'vitals/update_vitals.html', context)

@login_required(login_url='login')
def delete_vitals(request, vitals_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    vitals_instance = get_object_or_404(Vitals, id=vitals_id, patient=current_patient)

    if request.method == 'POST':
        vitals_instance.delete()
        messages.success(request, 'Vitals deleted successfully.')
        return redirect('view_vitals')

    context = {
        'vitals_instance': vitals_instance,
    }
    return render(request, 'vitals/delete_vitals.html', context)

@login_required(login_url='login')
def print_vitals_pdf(request, vitals_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    vitals_instance = get_object_or_404(Vitals, id=vitals_id, patient=current_patient)

    template_path = 'vitals/print_vitals.html'
    context = {'vitals_instance': vitals_instance}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="vitals_report.pdf"'

    # Create the PDF object, using the template and context
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If error during PDF creation, return the error message
    if pisa_status.err:
        return HttpResponse('Error creating PDF')
    return response

###################################
################  end vitals 
@login_required(login_url='login')
def newadd_medical_history(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)

    if request.method == 'POST':
        form = NEWMedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.patient = current_patient
            medical_history.save()
            messages.success(request, 'Medical history recorded successfully.')
            return redirect('newview_medical_history')
    else:
        form = NEWMedicalHistoryForm()

    context = {
        'form': form,
    }
    return render(request, 'medicalhistory/add_medical_historyy.html', context)

@login_required(login_url='login')
def newview_medical_history(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    medical_history_records = NewmedicalHistory.objects.filter(patient=current_patient)
    print([record.id for record in medical_history_records])  # Add this line

    context = {
        'medical_history_records': medical_history_records,
    }
    return render(request, 'medicalhistory/view_medical_history.html', context)

@login_required(login_url='login')
def update_medical_history(request, record_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    medical_record = get_object_or_404(NewmedicalHistory, id=record_id, patient=current_patient)

    if request.method == 'POST':
        form = NEWMedicalHistoryForm(request.POST, instance=medical_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical history updated successfully.')
            return redirect('newview_medical_history')
    else:
        form = NEWMedicalHistoryForm(instance=medical_record)

    context = {
        'form': form,
        'record_id': record_id,
    }
    return render(request, 'medicalhistory/update_medical_history.html', context)

############################################################################


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exercise, Dietary, Smoking, Alcohol, Medications, Lifestyle
from .forms import ExerciseForm, DietaryForm, SmokingForm, AlcoholForm, MedicationsForm, LifestyleForm
from .models import Patient
# views.py

from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exercise, Dietary, Smoking, Alcohol, Medications, Lifestyle
from .forms import ExerciseForm, DietaryForm, SmokingForm, AlcoholForm, MedicationsForm, LifestyleForm
from .models import Patient

# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exercise, Dietary, Smoking, Alcohol, Medications, Lifestyle
from .forms import ExerciseForm, DietaryForm, SmokingForm, AlcoholForm, MedicationsForm, LifestyleForm
from .models import Patient

@login_required(login_url='login')
def add_lifestyle_details(request):
    current_user = request.user

    if request.method == 'POST':
        exercise_form = ExerciseForm(request.POST)
        dietary_form = DietaryForm(request.POST)
        smoking_form = SmokingForm(request.POST)
        alcohol_form = AlcoholForm(request.POST)
        medications_form = MedicationsForm(request.POST)
        lifestyle_form = LifestyleForm(request.POST)

        if all(form.is_valid() for form in [exercise_form, dietary_form, smoking_form, alcohol_form, medications_form, lifestyle_form]):
            try:
                current_patient = Patient.objects.get(user=current_user)
                
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

                messages.success(request, 'Lifestyle details recorded successfully.')
                return redirect('patient_dashboard')
            
            except Patient.DoesNotExist:
                messages.error(request, 'Patient not found. Please make sure your account is associated with a patient.')
                return redirect('add_lifestyle_details')

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
    })


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Exercise, Dietary, Smoking, Alcohol, Medications, Lifestyle
from .models import Patient
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def view_lifestyle_details(request):
    current_user = request.user

    try:
        current_patient = Patient.objects.get(user=current_user)

        exercise_records = Exercise.objects.filter(patient=current_patient)
        dietary_records = Dietary.objects.filter(patient=current_patient)
        smoking_records = Smoking.objects.filter(patient=current_patient)
        alcohol_records = Alcohol.objects.filter(patient=current_patient)
        medications_records = Medications.objects.filter(patient=current_patient)
        lifestyle_records = Lifestyle.objects.filter(patient=current_patient)

        return render(request, 'view_lifestyle_details.html', {
            'exercise_records': exercise_records,
            'dietary_records': dietary_records,
            'smoking_records': smoking_records,
            'alcohol_records': alcohol_records,
            'medications_records': medications_records,
            'lifestyle_records': lifestyle_records,
        })

    except Patient.DoesNotExist:
        messages.error(request, 'Patient not found. Please make sure your account is associated with a patient.')
        return redirect('view_lifestyle_details')


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import MedicalHistory, TreatmentRecord
from .forms import MedicalHistoryyyForm, TreatmentRecordForm
from .models import Patient  # Adjust the import as needed

@login_required(login_url='login')
def add_medical_history(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)

    if request.method == 'POST':
        form = MedicalHistoryyyForm(request.POST)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.patient = current_patient
            medical_history.save()
            messages.success(request, 'Medical history added successfully.')
            return redirect('view_medical_history')
    else:
        form = MedicalHistoryyyForm()

    context = {
        'form': form,
    }
    return render(request, 'medical_history/add_medical_history.html', context)

@login_required(login_url='login')
def view_medical_history(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    medical_history_records = MedicalHistory.objects.filter(patient=current_patient)

    context = {
        'medical_history_records': medical_history_records,
    }
    return render(request, 'medical_history/view_medical_history.html', context)


# @login_required(login_url='login')
# def view_medical_history(request):
#     current_user = request.user
#     current_patient = Patient.objects.get(user=current_user)
#     medical_history_records = MedicalHistory.objects.filter(patient=current_patient)

#     context = {
#         'medical_history_records': medical_history_records,
#     }
#     return render(request, 'medical_history/view_medical_history.html', context)

@login_required(login_url='login')
def update_medical_history(request, medical_history_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    medical_history_instance = get_object_or_404(MedicalHistory, id=medical_history_id, patient=current_patient)

    if request.method == 'POST':
        form = MedicalHistoryyyForm(request.POST, instance=medical_history_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical history updated successfully.')
            return redirect('view_medical_history')
    else:
        form = MedicalHistoryyyForm(instance=medical_history_instance)

    context = {
        'form': form,
    }
    return render(request, 'medical_history/update_medical_history.html', context)

@login_required(login_url='login')
def delete_medical_history(request, medical_history_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    medical_history_instance = get_object_or_404(MedicalHistory, id=medical_history_id, patient=current_patient)

    if request.method == 'POST':
        medical_history_instance.delete()
        messages.success(request, 'Medical history deleted successfully.')
        return redirect('view_medical_history')

    context = {
        'medical_history_instance': medical_history_instance,
    }
    return render(request, 'medical_history/delete_medical_history.html', context)

@login_required(login_url='login')
def print_medical_history_pdf(request, medical_history_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    medical_history_instance = get_object_or_404(MedicalHistory, id=medical_history_id, patient=current_patient)

    template_path = 'print_medical_history.html'
    context = {'medical_history_instance': medical_history_instance}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="medical_history_report.pdf"'

    # Create the PDF object, using the template and context
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If error during PDF creation, return the error message
    if pisa_status.err:
        return HttpResponse('Error creating PDF')
    return response
# views.py
############################################
@login_required(login_url='login')
def add_treatment_record(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)

    if request.method == 'POST':
        form = TreatmentRecordForm(request.POST)
        if form.is_valid():
            treatment_record = form.save(commit=False)
            treatment_record.patient = current_patient
            treatment_record.save()
            messages.success(request, 'Treatment record added successfully.')
            return redirect('view_treatment_records')
    else:
        form = TreatmentRecordForm()

    context = {
        'form': form,
    }
    return render(request, 'treatment_records/add_treatment_record.html', context)

@login_required(login_url='login')
def view_treatment_records(request):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    treatment_records = TreatmentRecord.objects.filter(patient=current_patient)

    context = {
        'treatment_records': treatment_records,
    }
    return render(request, 'treatment_records/view_treatment_records.html', context)

@login_required(login_url='login')
def update_treatment_record(request, treatment_record_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    treatment_record_instance = get_object_or_404(TreatmentRecord, id=treatment_record_id, patient=current_patient)

    if request.method == 'POST':
        form = TreatmentRecordForm(request.POST, instance=treatment_record_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Treatment record updated successfully.')
            return redirect('view_treatment_records')
    else:
        form = TreatmentRecordForm(instance=treatment_record_instance)

    context = {
        'form': form,
    }
    return render(request, 'treatment_records/update_treatment_record.html', context)

@login_required(login_url='login')
def delete_treatment_record(request, treatment_record_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    treatment_record_instance = get_object_or_404(TreatmentRecord, id=treatment_record_id, patient=current_patient)

    if request.method == 'POST':
        treatment_record_instance.delete()
        messages.success(request, 'Treatment record deleted successfully.')
        return redirect('view_treatment_records')

    context = {
        'treatment_record_instance': treatment_record_instance,
    }
    return render(request, 'treatment_records/delete_treatment_record.html', context)

@login_required(login_url='login')
def print_treatment_record_pdf(request, treatment_record_id):
    current_user = request.user
    current_patient = Patient.objects.get(user=current_user)
    treatment_record_instance = get_object_or_404(TreatmentRecord, id=treatment_record_id, patient=current_patient)

    template_path = 'print_treatment_record.html'
    context = {'treatment_record_instance': treatment_record_instance}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="treatment_record_report.pdf"'

    # Create the PDF object, using the template and context
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If error during PDF creation, return the error message
    if pisa_status.err:
        return HttpResponse('Error creating PDF')
    return response

# Similar views for TreatmentRecord (add, view, update, delete, and print)
# Make sure to adjust the model, form, and template names accordingly.


# def add_medical_history(request):
#     if request.method == 'POST':
#         medical_history_form = MedicalHistoryyyForm(request.POST)
#         treatment_record_form = TreatmentRecordForm(request.POST)

#         if medical_history_form.is_valid() and treatment_record_form.is_valid():
#             medical_history = medical_history_form.save(commit=False)
#             treatment_record = treatment_record_form.save()
#             medical_history.save()
#             medical_history.treatment_records.add(treatment_record)

#             return redirect('medical_history_list') 
#     else:
#         medical_history_form = MedicalHistoryyyForm()
#         treatment_record_form = TreatmentRecordForm()

#     return render(request, 'medicalhistory/add_medical_history.html', {'medical_history_form': medical_history_form, 'treatment_record_form': treatment_record_form})

# def medical_history_detail(request, medical_history_id):
#     medical_history = get_object_or_404(MedicalHistory, pk=medical_history_id)
#     return render(request, 'medicalhistory/medical_history_detail.html', {'medical_history': medical_history})

# def medical_history_list(request):
#     medical_histories = MedicalHistory.objects.all()
#     return render(request, 'medicalhistory/medical_history_list.html', {'medical_histories': medical_histories})
##################################33

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
        return render(request, 'goals/add_health_goal.html', context)
    else:
        # Handle unauthenticated user
        return redirect('login')
###################################################
def health_goal_list(request):
    if request.user.is_authenticated:
        patient = Patient.objects.get(user=request.user)
        health_goals = patient.health_goals.all()

        context = {'health_goals': health_goals}
        return render(request, 'goals/display_health_goals.html', context)
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





def Medication(request, patient_id):
    try:
        current_user = request.user
        patient = get_object_or_404(Patient, id=patient_id)
        current_doctor = get_object_or_404(Doctor, user=current_user)
        doctor_for_patient = MedicalHistoryy.objects.get(patient=patient, doctor=current_doctor)
        accepted_patient = MedicalHistoryy.objects.get(id=patient_id)
        speciality = DoctorSpecialization.objects.get(doctor=current_doctor)
        if request.method == 'POST':
            form = MedicalTreatmentForm(request.POST)
            if form.is_valid():
                medical_history = form.save(commit=False)
                medical_history.patient = patient
                medical_history.doctor = current_doctor
                medical_history.save()
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
        return HttpResponseBadRequest("Patient not found")
    except Doctor.DoesNotExist:
        return HttpResponseBadRequest("Doctor not found")


def generate_medical_treatment_pdf(request, patient_id):
    try:
        current_doctor = request.user
        current_doctor = get_object_or_404(Doctor, user=current_doctor)
        patient = get_object_or_404(Patient, id=patient_id)
        medical_history_records = Medical_History.objects.filter(patient=patient)
        buffer = BytesIO()
        c = canvas.Canvas(buffer)
        c.setTitle("Medical Treatment Report")
        c.setAuthor("Your Name")
        c.setSubject("Medical Treatment Report for " + patient.user.first_name)
        text = c.beginText()
        text.setFont("Helvetica", 12)
        text.setTextOrigin(50, 750)  
        text.textLine("Patient: " + patient.user.first_name)
        text.textLine("doctor: " + current_doctor.user.first_name)
        text.textLine("Date: " + str(datetime.date.today())) 
        text.textLine("\nMedical Treatment Records:")
        for record in medical_history_records:
            text.textLine("- History: " + record.history)
            text.textLine("- Follow-up Date: " + str(record.follow_up_date))
            text.textLine("- Payment Type: " + record.payment_type.name)
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
        c.showPage()
        c.save()
        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename="medical_treatment_report.pdf")
        return response
    except Patient.DoesNotExist:
        return HttpResponseBadRequest("Patient not found")



def lab_report_confirmation(request, lab_report_id):
    lab_report = get_object_or_404(LabReport, id=lab_report_id)

    context = {
        'lab_report': lab_report,
    }

    return render(request, 'labreport/lab_report_confirmation.html', context)

def lab_report(request, patient_id):
    try:
        current_user = request.user
        print(f'Current User: {current_user}')  
        patient = get_object_or_404(Patient, id=patient_id)
        print(f'Patient: {patient}')  
        current_doctor = get_object_or_404(Doctor, user=current_user)
        print(f'Current Doctor: {current_doctor}') 
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

