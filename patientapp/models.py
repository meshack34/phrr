from datetime import date, datetime
from django.utils import timezone
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import redirect
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .models import *
# Add these imports to the top of your models.py
from django.core.validators import MaxValueValidator, MinValueValidator

class AccountManager(BaseUserManager):
    
    def create_user(self, first_name, last_name, username, email, password=None, account_id=None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            account_id=account_id,
            **extra_fields,  # Include additional fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,  # Include additional fields
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
        

    def get_account_by_security_answers(self, security_question_1, security_answer_1, security_question_2, security_answer_2):
        try:
            return self.get(
                security_question_1=security_question_1,
                security_answer_1=security_answer_1,
                security_question_2=security_question_2,
                security_answer_2=security_answer_2,
            )
        except self.model.DoesNotExist:
            return None
        
class Account(AbstractBaseUser):
    email           = models.EmailField(max_length=100, unique=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    phone_number    = models.CharField(max_length=50)
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_superadmin        = models.BooleanField(default=False)

    account_id = models.CharField(max_length=32, unique=True)  
    security_question_1 = models.CharField(max_length=100, blank=True, null=True)
    security_answer_1 = models.CharField(max_length=100, blank=True, null=True)

    security_question_2 = models.CharField(max_length=100, blank=True, null=True)
    security_answer_2 = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'account_id'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
class EmergencyContact(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='emergency_contact')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    home_address = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.relationship}"

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    profile_image = models.ImageField(upload_to='patients/%Y/%m/%d/', default='default.png')
    emergency_contact = models.OneToOneField(EmergencyContact, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    blood_group = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True)
    date_joined = models.DateTimeField(default=date.today, blank=True)
    date_of_birth = models.DateField(null=True)
    age_years = models.PositiveIntegerField(null=True)  

    @property
    def calculate_age(self):  # Rename the property
        today = date.today()
        if self.date_of_birth:
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return None
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'



class HealthcareSpecialty(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Healthcare Specialty'
        verbose_name_plural = 'Healthcare Specialties'

class HealthcareProfessional(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='healthcare_professionals')
    profile_image = models.ImageField(upload_to='healthcare_professionals/%Y/%m/%d/', default='default.png')
    name = models.CharField(max_length=255)
    health_facility = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    speciality = models.ForeignKey(HealthcareSpecialty, on_delete=models.CASCADE)
    address = models.TextField()
    working_hours = models.CharField(max_length=255)
    education = models.TextField()
    experience_years = models.PositiveIntegerField()
    certifications = models.TextField()
    services_offered = models.TextField()
    languages_spoken = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    insurance_accepted = models.TextField()
    appointment_booking_info = models.TextField()
    patient_reviews = models.TextField()
    professional_memberships = models.TextField()
    additional_notes = models.TextField()


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Healthcare Professional'
        verbose_name_plural = 'Healthcare Professionals'

class Allergy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    allergy_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    diagnosis_date = models.DateField()

    def __str__(self):
        return f'{self.allergy_name} - {self.severity}'
    
class Medication(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dosage = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.dosage}'

class NewmedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(auto_now_add=True)
    chief_complaint = models.TextField()
    present_illness = models.TextField()
    past_medical_history = models.TextField()
    allergies = models.ManyToManyField(Allergy, blank=True)
    medications = models.ManyToManyField(Medication, blank=True)
    family_history = models.TextField(blank=True, null=True)
    social_history = models.TextField(blank=True, null=True)
    
    # Additional details
    surgical_history = models.TextField(blank=True, null=True)
    immunization_history = models.TextField(blank=True, null=True)
    occupational_history = models.TextField(blank=True, null=True)
    review_of_systems = models.TextField(blank=True, null=True)
    physical_examination = models.TextField(blank=True, null=True)
    lab_results = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Medical History for {self.patient.user.username} - {self.date_recorded}'


class Vitals(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(30), MaxValueValidator(45)])
    heart_rate = models.PositiveIntegerField(validators=[MinValueValidator(30), MaxValueValidator(200)])
    blood_pressure_systolic = models.PositiveIntegerField(validators=[MinValueValidator(60), MaxValueValidator(250)])
    blood_pressure_diastolic = models.PositiveIntegerField(validators=[MinValueValidator(40), MaxValueValidator(150)])
    respiratory_rate = models.PositiveIntegerField(validators=[MinValueValidator(8), MaxValueValidator(40)])
    oxygen_saturation = models.PositiveIntegerField(validators=[MinValueValidator(80), MaxValueValidator(100)])

    def __str__(self):
        return f'Vitals Record for {self.patient.user.username} - {self.date_recorded}'

#####################################

class Doctor(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)  
    date_joined = models.DateTimeField(default=date.today, blank=True)
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True)
    address  = models.CharField(max_length=50)
    date_joined = models.DateTimeField(default=datetime.now, blank=True)
    profile_image = models.ImageField(upload_to='doctors/%Y/%m/%d/',default='default.png')
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    

class DoctorSpecialization(models.Model):
    doctor_category  = models.CharField(max_length=50, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.doctor_category




# for when patient select appoint time from patient dashboard
class PatientAppointment(models.Model):
    appoint_date = models.CharField(max_length=50, null=True)
    appoint_time = models.CharField(max_length=50, null=True)
    appoint_day = models.CharField(max_length=50, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
    month = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.patient


# for doctor only. Doc will select time slot for his/her appointment
class AppointmentTime(models.Model):
    day = models.CharField(max_length=50, null=True)
    time_from = models.CharField(max_length=50, null=True)
    time_to = models.CharField(max_length=50, null=True)
    from_to = models.CharField(max_length=50, null=True)
    appointment_date = models.DateField(null=True)
    month = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=50, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.day


    

class MedicalRecords(models.Model):
    medical_insurance =  models.FileField(upload_to='insurance/%Y/% m/% d/')
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
    class Meta:
        verbose_name_plural = "MedicalRecords"

    def __str__(self):
        return self.patient.user.first_name



class CurrentMedication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    reason = models.CharField(max_length=200)
    date = models.DateField()



class Surgery(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    surgery_type = models.CharField(max_length=100)
    surgery_date = models.DateField()
    reason = models.CharField(max_length=200)

class ImmunizationHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=100)
    date = models.DateField()

class FamilyMedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medical_condition = models.CharField(max_length=100)
    affected_member_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)

class MedicalHistoryy(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    reason =  models.CharField(max_length=200, blank=True)
    ever_had = models.CharField(max_length=200,blank=True)
    
    weight = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, null=True)
    blood_group = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)
    age_years = models.PositiveIntegerField(null=True)
    
    other_illness = models.CharField(max_length=200,blank=True)
    other_information = models.CharField(max_length=200,blank=True)
    is_processing = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now, blank=True)

    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name_plural = "MedicalHistories"

   


class Prescription(models.Model):
    name =  models.CharField(max_length=50, null=True)
    quantity  = models.CharField(max_length=50, null=True)
    days = models.CharField(max_length=50, null=True)
    morning = models.CharField(max_length=10, null=True)
    afternoon = models.CharField(max_length=10, null=True)
    evening = models.CharField(max_length=10, null=True)
    night = models.CharField(max_length=10, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
    uploaded_date = models.DateTimeField(default=datetime.now, blank=True)
    def __int__(self):
        return self.id
   
class PrescriptionStatus(models.Model):
    is_uploaded= models.BooleanField(default=False)
    newprescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)

    def __int__(self):
        return self.id

class Treatment(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    def __str__(self):
        return f'{self.name} - {self.price}'
    
class ReviewofSystem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    def __str__(self):
        return f'{self.name} - {self.price}'
    

class Examination(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    def __str__(self):
        return f'{self.name} - {self.price}'
    
class Diagnosis(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    def __str__(self):
        return f'{self.name} - {self.price}'
    
class Investigation(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    def __str__(self):
        return f'{self.name} - {self.price}'
    
class Consultation(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    def __str__(self):
        return f'{self.name} - {self.price}'
       

    
class PaymentType(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Medical_History(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
    history = models.CharField(max_length=255)
    review_of_systems = models.ManyToManyField(ReviewofSystem)
    examination = models.ManyToManyField(Examination)
    diagnosis = models.ManyToManyField(Diagnosis)
    treatment = models.ManyToManyField(Treatment)
    investigation = models.ManyToManyField(Investigation)
    medication = models.ManyToManyField(Medication)
    consultation = models.ManyToManyField(Consultation)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    follow_up_date = models.DateField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.patient.user.first_name} - {self.patient.user.last_name}'
    def calculate_total_price(self):
    # Calculate total price based on selected categories, categories2, and categories3
        total_price = sum(category.price for category in self.review_of_systems.all())
        total_price += sum(category.price for category in self.examination.all())
        total_price += sum(category.price for category in self.diagnosis.all())
        total_price += sum(category.price for category in self.treatment.all())
        total_price += sum(category.price for category in self.investigation.all())
        total_price += sum(category.price for category in self.medication.all())
        total_price += sum(category.price for category in self.consultation.all())
        return total_price
    

    class Meta:
        verbose_name_plural = 'Medical History'


class Appointment(models.Model):
    appointment_date  = models.DateField(null=True)
    appointment_status  = models.BooleanField(default='inactive')
    booking_date  = models.DateField(null=True)
    followup_date  = models.DateField(null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.patient.user.first_name

class LabReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    test_result = models.DecimalField(max_digits=10, decimal_places=2)
    test_unit = models.CharField(max_length=20)
    normal_range_min = models.DecimalField(max_digits=10, decimal_places=2)
    normal_range_max = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    specimen_type = models.CharField(max_length=50)
    collection_date_time = models.DateTimeField()
    lab_name = models.CharField(max_length=100)
    report_number = models.CharField(max_length=20)
    report_generated_date_time = models.DateTimeField()
    signature = models.CharField(max_length=100)
    credentials = models.CharField(max_length=100)
    additional_notes = models.TextField()
    barcode = models.CharField(max_length=50)



class Exercise(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=50, blank=True, null=True)
    exercise_duration = models.IntegerField(blank=True, null=True)
    exercise_frequency = models.CharField(max_length=50, blank=True, null=True)

class Dietary(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dietary_preferences = models.CharField(max_length=50, blank=True, null=True)
    food_allergies = models.CharField(max_length=100, blank=True, null=True)
    balanced_diet = models.TextField(blank=True, null=True)

class Smoking(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    SMOKING_STATUS_CHOICES = [
        ('current', 'Current'),
        ('former', 'Former'),
    ]
    smoking_status = models.CharField(max_length=20, choices=SMOKING_STATUS_CHOICES, blank=True, null=True)
    quit_date = models.DateField(blank=True, null=True)
    cigarettes_per_day = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.smoking_status == 'current':
            self.quit_date = None  
        elif self.smoking_status == 'former':
            self.cigarettes_per_day = None 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient: {self.patient}, Smoking Status: {self.smoking_status}"

class Alcohol(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    alcohol_consumption = models.BooleanField(default=False)
    alcohol_frequency = models.CharField(max_length=20, blank=True, null=True)
    alcohol_types = models.CharField(max_length=100, blank=True, null=True)
    alcohol_units_per_week = models.IntegerField(blank=True, null=True)

class Medications(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medications = models.CharField(max_length=50, blank=True, null=True)
    medication_dosage = models.CharField(max_length=50, blank=True, null=True)
    medication_instructions = models.TextField(blank=True, null=True)

class Lifestyle(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    occupational_exposures = models.TextField(blank=True, null=True)



class HealthInsurance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_insurances',)
    company_name = models.CharField(max_length=100)
    policy_member_id = models.CharField(max_length=100)
    group_number = models.CharField(max_length=100, blank=True, null=True)
    coverage_dates = models.DateField(null=True, blank=True)  
    contact_information = models.TextField()
    policy_holder_name = models.CharField(max_length=100, blank=True, null=True)
    policy_holder_relationship = models.CharField(max_length=50, blank=True, null=True)
    insurance_card_image = models.ImageField(upload_to='insurance_cards/', blank=True, null=True)

    def __str__(self):
        return self.company_name



class HealthGoal(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('complete', 'Complete'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_goals')
    goal_description = models.CharField(max_length=200)
    target_date = models.DateField()
    progress = models.IntegerField(default=0, help_text="Progress in percentage")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    
class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    condition_name = models.CharField(max_length=100)
    diagnosis_date = models.DateField()
    is_current = models.BooleanField(default=True)
    treatment_records = models.ManyToManyField('TreatmentRecord')

    def is_past_condition(self):
        return not self.is_current

class TreatmentRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatment_records')
    prescribed_medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    monitoring_schedule = models.TextField()
    results = models.TextField()
    date_recorded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Medication: {self.prescribed_medication}, Start Date: {self.start_date}"
