from .models import *
from django.forms import DateInput
from django.forms.fields import DateField
from django.forms.widgets import PasswordInput
from django import forms
from django.forms import DateInput, DateField, PasswordInput
from django import forms
from django.forms import PasswordInput

from .models import Account
from .models import HealthInsurance
from .models import MedicalHistory, TreatmentRecord
from django import forms
from .models import Exercise, Dietary, Smoking, Alcohol, Medications, Lifestyle,HealthcareProfessional,HealthcareSpecialty
from .models import HealthGoal
from django import forms
from .models import EmergencyContact
from .models import Vitals
from .models import HealthcareProfessional
from django import forms
from .models import NewmedicalHistory
from django import forms
from .models import MedicalHistory, Allergy, Medication
from django import forms
from .models import Surgery         
from django import forms
from .models import Allergy



class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ['allergy_name', 'severity', 'diagnosis_date']

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'start_date', 'end_date']

class NEWMedicalHistoryForm(forms.ModelForm):
    allergies = forms.ModelMultipleChoiceField(
        queryset=Allergy.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    medications = forms.ModelMultipleChoiceField(
        queryset=Medication.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = NewmedicalHistory
        fields = ['chief_complaint', 'present_illness', 'past_medical_history', 'allergies', 'medications', 'family_history', 'social_history', 'surgical_history', 'immunization_history', 'occupational_history', 'review_of_systems', 'physical_examination', 'lab_results']

            
class MedicalTreatmentForm(forms.ModelForm):
    treatment = forms.ModelMultipleChoiceField(queryset=Treatment.objects.all(), widget=forms.CheckboxSelectMultiple)
    review_of_systems = forms.ModelMultipleChoiceField(queryset=ReviewofSystem.objects.all(), widget=forms.CheckboxSelectMultiple)
    examination = forms.ModelMultipleChoiceField(queryset=Examination.objects.all(), widget=forms.CheckboxSelectMultiple)
    diagnosis = forms.ModelMultipleChoiceField(queryset=Diagnosis.objects.all(), widget=forms.CheckboxSelectMultiple)
    investigation = forms.ModelMultipleChoiceField(queryset=Investigation.objects.all(), widget=forms.CheckboxSelectMultiple)
    medication = forms.ModelMultipleChoiceField(queryset=Medication.objects.all(), widget=forms.CheckboxSelectMultiple)
    consultation = forms.ModelMultipleChoiceField(queryset=Consultation.objects.all(), widget=forms.CheckboxSelectMultiple)
    follow_up_date = DateField(widget=DateInput)
    class Meta:
        model = Medical_History
        fields = ('__all__')
        


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    security_question_1 = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    security_answer_1 = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    security_question_2 = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    security_answer_2 = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        # Set form-control class for all fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


# forms.py

class AdditionalUserForm(forms.ModelForm):
    class Meta:
        model = AdditionalUser
        exclude = ['account_id'] 
        fields = '__all__'
from django import forms
from .models import DoctorNote

class DoctorNoteForm(forms.ModelForm):
    class Meta:
        model = DoctorNote
        fields = '__all__'


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['profile_image', 'city', 'address', 'country', 'date_of_birth', 'blood_group', 'gender']

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs['class'] = 'upload'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control'


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone_number', 'email_address', 'home_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['relationship'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['email_address'].widget.attrs['class'] = 'form-control'
        self.fields['home_address'].widget.attrs['class'] = 'form-control'




from django import forms
from .models import HealthcareProfessional, HealthcareSpecialty


class HealthcareProfessionalForm(forms.ModelForm):
    class Meta:
        model = HealthcareProfessional
        fields = ['name', 'health_facility', 'phone', 'email', 'speciality', 'address', 'working_hours',
                  'education', 'experience_years', 'certifications', 'services_offered', 'languages_spoken',
                  'emergency_contact', 'insurance_accepted', 'appointment_booking_info', 'patient_reviews',
                  'professional_memberships', 'additional_notes']
        widgets = {
            'working_hours': forms.TextInput(attrs={'placeholder': 'e.g., Monday-Friday 9 AM - 5 PM'}),
            'education': forms.Textarea(attrs={'placeholder': 'Enter education details here'}),
            'certifications': forms.Textarea(attrs={'placeholder': 'Enter certifications here'}),
            'services_offered': forms.Textarea(attrs={'placeholder': 'Enter services offered here'}),
            'languages_spoken': forms.Textarea(attrs={'placeholder': 'Enter languages spoken here'}),
            'insurance_accepted': forms.Textarea(attrs={'placeholder': 'Enter accepted insurances here'}),
            'appointment_booking_info': forms.Textarea(attrs={'placeholder': 'Enter booking information here'}),
            'patient_reviews': forms.Textarea(attrs={'placeholder': 'Enter patient reviews here'}),
            'professional_memberships': forms.Textarea(attrs={'placeholder': 'Enter professional memberships here'}),
            'additional_notes': forms.Textarea(attrs={'placeholder': 'Enter additional notes here'}),
        }

    # Override the default behavior to make only 'name', 'phone', and 'email' mandatory
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['phone'].required = True
        self.fields['email'].required = True


class HealthInsuranceForm(forms.ModelForm):
    class Meta:
        model = HealthInsurance
        fields = ['company_name', 'policy_member_id', 'group_number', 'coverage_dates',
                  'contact_information', 'policy_holder_name', 'policy_holder_relationship',
                  'insurance_card_image']
 
class MedicalHistoryyyForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class TreatmentRecordForm(forms.ModelForm):
    class Meta:
        model = TreatmentRecord
        fields = '__all__'


class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = '__all__'
        

class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        fields = ['temperature', 'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'respiratory_rate', 'oxygen_saturation']

##################################

# forms.py

# forms.py
# forms.py

from django import forms
from .models import PatientDischarge

class PatientDischargeForm(forms.ModelForm):
    class Meta:
        model = PatientDischarge
        exclude = []  # You can exclude fields if needed

from django import forms
from .models import Exercise, Dietary, Smoking, Alcohol, Medications, Lifestyle

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise_type', 'exercise_duration', 'exercise_frequency']

class DietaryForm(forms.ModelForm):
    class Meta:
        model = Dietary
        fields = ['dietary_preferences', 'food_allergies', 'balanced_diet']

class SmokingForm(forms.ModelForm):
    class Meta:
        model = Smoking
        fields = ['smoking_status', 'quit_date', 'cigarettes_per_day']

class AlcoholForm(forms.ModelForm):
    class Meta:
        model = Alcohol
        fields = ['alcohol_consumption', 'alcohol_frequency', 'alcohol_types', 'alcohol_units_per_week']

class MedicationsForm(forms.ModelForm):
    class Meta:
        model = Medications
        fields = ['medications', 'medication_dosage', 'medication_instructions']

class LifestyleForm(forms.ModelForm):
    class Meta:
        model = Lifestyle
        fields = ['occupational_exposures']


#######################

class HealthcareSpecialityForm(forms.ModelForm):
    class Meta:
        model = HealthcareSpecialty
        fields = '__all__'


class HealthcareExpertForm(forms.ModelForm):
    class Meta:
        model = HealthcareProfessional
        fields = '__all__'
# insurance_app/forms.py


##############################################################################################

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address', 'profile_image', 'gender', 'description']

class DoctorSpecilizationForm(forms.ModelForm):
    class Meta:
        model = DoctorSpecialization
        fields = ['doctor_category',]

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].widget.attrs['class'] = 'upload'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['gender'].widget.attrs['class'] = 'form-control select'
        self.fields['description'].widget.attrs['class'] = 'form-control'



class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistoryy
        fields = [
            'reason',
            'weight',
            'other_illness',
            'other_information',
        ]

    def __init__(self, *args, **kwargs):
        super(MedicalHistoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


from django import forms

class FamilyMedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = FamilyMedicalHistory
        fields = [
            'medical_condition',
            'affected_member_name',
            'relationship',
        ]

    def __init__(self, *args, **kwargs):
        super(FamilyMedicalHistoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
from django import forms
from .models import CurrentMedication

class CurrentMedicationForm(forms.ModelForm):
    class Meta:
        model = CurrentMedication
        fields = [
            'medicine_name',
            'reason',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        super(CurrentMedicationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
 

class SurgeryForm(forms.ModelForm):
    class Meta:
        model = Surgery
        fields = [
            'surgery_type',
            'surgery_date',
            'reason',
        ]

    def __init__(self, *args, **kwargs):
        super(SurgeryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
from django import forms
from .models import ImmunizationHistory

class ImmunizationHistoryForm(forms.ModelForm):
    class Meta:
        model = ImmunizationHistory
        fields = [
            'vaccine_name',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        super(ImmunizationHistoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class FamilyMedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = FamilyMedicalHistory
        fields = [
            'medical_condition',
            'affected_member_name',
            'relationship',
        ]

    def __init__(self, *args, **kwargs):
        super(FamilyMedicalHistoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
from django import forms
from .models import LabReport

class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        exclude = ['patient', 'doctor']  # Exclude patient and doctor fields from the form



#