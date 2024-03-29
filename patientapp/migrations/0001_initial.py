# Generated by Django 4.2.5 on 2023-12-19 08:45

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=100)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('account_id', models.CharField(max_length=32, unique=True)),
                ('security_question_1', models.CharField(blank=True, max_length=100, null=True)),
                ('security_answer_1', models.CharField(blank=True, max_length=100, null=True)),
                ('security_question_2', models.CharField(blank=True, max_length=100, null=True)),
                ('security_answer_2', models.CharField(blank=True, max_length=100, null=True)),
                ('password_reset_token', models.CharField(blank=True, max_length=255, null=True)),
                ('password_reset_token_created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdditionalUser',
            fields=[
                ('additional_user_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=100)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('security_question_1', models.CharField(blank=True, max_length=100, null=True)),
                ('security_answer_1', models.CharField(blank=True, max_length=100, null=True)),
                ('security_question_2', models.CharField(blank=True, max_length=100, null=True)),
                ('security_answer_2', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(max_length=128)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='additional_user_profiles/')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_users_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergy_name', models.CharField(max_length=100)),
                ('severity', models.CharField(max_length=50)),
                ('diagnosis_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True)),
                ('address', models.CharField(max_length=50)),
                ('date_joined', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('profile_image', models.ImageField(default='default.png', upload_to='doctors/%Y/%m/%d/')),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('relationship', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('email_address', models.EmailField(max_length=254)),
                ('home_address', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_contact', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HealthcareSpecialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Healthcare Specialty',
                'verbose_name_plural': 'Healthcare Specialties',
            },
        ),
        migrations.CreateModel(
            name='Investigation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('dosage', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nursing_Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uhid', models.CharField(max_length=30)),
                ('patient_name', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('diagnosis', models.CharField(max_length=100)),
                ('hosp_no', models.CharField(max_length=100)),
                ('chemotherapy_protocol', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Nursing_Notes_sub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uhid', models.CharField(max_length=30)),
                ('date_time', models.CharField(max_length=100)),
                ('nursing_notes', models.CharField(max_length=100)),
                ('name_sign', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='default.png', upload_to='patients/%Y/%m/%d/')),
                ('city', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True)),
                ('blood_group', models.CharField(max_length=50, null=True)),
                ('date_joined', models.DateTimeField(blank=True, default=datetime.date.today)),
                ('date_of_birth', models.DateField(null=True)),
                ('age_years', models.PositiveIntegerField(null=True)),
                ('emergency_contact', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patientapp.emergencycontact')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PatientDischarge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.CharField(max_length=200)),
                ('date_time', models.DateTimeField()),
                ('patient_name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('date_of_admission', models.DateField()),
                ('date_of_discharge', models.DateField()),
                ('discharge_diagnosis', models.TextField()),
                ('procedures_and_therapies', models.TextField(blank=True, null=True)),
                ('complications', models.TextField()),
                ('consultations', models.TextField()),
                ('patient_history', models.TextField()),
                ('lab', models.TextField()),
                ('condition_of_discharge', models.TextField()),
                ('dispositions', models.TextField()),
                ('discharge_to', models.TextField()),
                ('diet', models.TextField()),
                ('activity', models.TextField()),
                ('dme', models.TextField()),
                ('home_health_services', models.TextField()),
                ('fu_apts', models.TextField(blank=True, null=True)),
                ('meds', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('quantity', models.CharField(max_length=50, null=True)),
                ('days', models.CharField(max_length=50, null=True)),
                ('morning', models.CharField(max_length=10, null=True)),
                ('afternoon', models.CharField(max_length=10, null=True)),
                ('evening', models.CharField(max_length=10, null=True)),
                ('night', models.CharField(max_length=10, null=True)),
                ('uploaded_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewofSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vitals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_recorded', models.DateTimeField(auto_now_add=True)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(45)])),
                ('heart_rate', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(200)])),
                ('blood_pressure_systolic', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(60), django.core.validators.MaxValueValidator(250)])),
                ('blood_pressure_diastolic', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(40), django.core.validators.MaxValueValidator(150)])),
                ('respiratory_rate', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(8), django.core.validators.MaxValueValidator(40)])),
                ('oxygen_saturation', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(80), django.core.validators.MaxValueValidator(100)])),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='TreatmentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescribed_medication', models.CharField(max_length=100)),
                ('dosage', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('monitoring_schedule', models.TextField()),
                ('results', models.TextField()),
                ('date_recorded', models.DateTimeField(default=django.utils.timezone.now)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment_records', to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Surgery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surgery_type', models.CharField(max_length=100)),
                ('surgery_date', models.DateField()),
                ('reason', models.CharField(max_length=200)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Smoking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smoking_status', models.CharField(blank=True, choices=[('current', 'Current'), ('former', 'Former')], max_length=20, null=True)),
                ('quit_date', models.DateField(blank=True, null=True)),
                ('cigarettes_per_day', models.IntegerField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_uploaded', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patientapp.doctor')),
                ('newprescription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patientapp.prescription')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='PatientAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appoint_date', models.CharField(max_length=50, null=True)),
                ('appoint_time', models.CharField(max_length=50, null=True)),
                ('appoint_day', models.CharField(max_length=50, null=True)),
                ('month', models.CharField(max_length=50, null=True)),
                ('date', models.CharField(max_length=50, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='NewmedicalHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_recorded', models.DateTimeField(auto_now_add=True)),
                ('chief_complaint', models.TextField()),
                ('present_illness', models.TextField()),
                ('past_medical_history', models.TextField()),
                ('family_history', models.TextField(blank=True, null=True)),
                ('social_history', models.TextField(blank=True, null=True)),
                ('surgical_history', models.TextField(blank=True, null=True)),
                ('immunization_history', models.TextField(blank=True, null=True)),
                ('occupational_history', models.TextField(blank=True, null=True)),
                ('review_of_systems', models.TextField(blank=True, null=True)),
                ('physical_examination', models.TextField(blank=True, null=True)),
                ('lab_results', models.TextField(blank=True, null=True)),
                ('allergies', models.ManyToManyField(blank=True, to='patientapp.allergy')),
                ('medications', models.ManyToManyField(blank=True, to='patientapp.medication')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Medications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medications', models.CharField(blank=True, max_length=50, null=True)),
                ('medication_dosage', models.CharField(blank=True, max_length=50, null=True)),
                ('medication_instructions', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_insurance', models.FileField(upload_to='insurance/%Y/% m/% d/')),
                ('date_created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.patient')),
            ],
            options={
                'verbose_name_plural': 'MedicalRecords',
            },
        ),
        migrations.CreateModel(
            name='MedicalHistoryy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20, null=True)),
                ('reason', models.CharField(blank=True, max_length=200)),
                ('ever_had', models.CharField(blank=True, max_length=200)),
                ('weight', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('blood_group', models.CharField(max_length=50, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('age_years', models.PositiveIntegerField(null=True)),
                ('other_illness', models.CharField(blank=True, max_length=200)),
                ('other_information', models.CharField(blank=True, max_length=200)),
                ('is_processing', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patientapp.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.patient')),
            ],
            options={
                'verbose_name_plural': 'MedicalHistories',
            },
        ),
        migrations.CreateModel(
            name='MedicalHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_name', models.CharField(max_length=100)),
                ('diagnosis_date', models.DateField()),
                ('is_current', models.BooleanField(default=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_histories', to='patientapp.patient')),
                ('treatment_records', models.ManyToManyField(to='patientapp.treatmentrecord')),
            ],
        ),
        migrations.CreateModel(
            name='Medical_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.CharField(max_length=255)),
                ('follow_up_date', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('consultation', models.ManyToManyField(to='patientapp.consultation')),
                ('diagnosis', models.ManyToManyField(to='patientapp.diagnosis')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='patientapp.doctor')),
                ('examination', models.ManyToManyField(to='patientapp.examination')),
                ('investigation', models.ManyToManyField(to='patientapp.investigation')),
                ('medication', models.ManyToManyField(to='patientapp.medication')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.patient')),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.paymenttype')),
                ('review_of_systems', models.ManyToManyField(to='patientapp.reviewofsystem')),
                ('treatment', models.ManyToManyField(to='patientapp.treatment')),
            ],
            options={
                'verbose_name_plural': 'Medical History',
            },
        ),
        migrations.CreateModel(
            name='Lifestyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupational_exposures', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='LabReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=100)),
                ('test_result', models.DecimalField(decimal_places=2, max_digits=10)),
                ('test_unit', models.CharField(max_length=20)),
                ('normal_range_min', models.DecimalField(decimal_places=2, max_digits=10)),
                ('normal_range_max', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=20)),
                ('specimen_type', models.CharField(max_length=50)),
                ('collection_date_time', models.DateTimeField()),
                ('lab_name', models.CharField(max_length=100)),
                ('report_number', models.CharField(max_length=20)),
                ('report_generated_date_time', models.DateTimeField()),
                ('signature', models.CharField(max_length=100)),
                ('credentials', models.CharField(max_length=100)),
                ('additional_notes', models.TextField()),
                ('barcode', models.CharField(max_length=50)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='ImmunizationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='HealthInsurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('policy_member_id', models.CharField(max_length=100)),
                ('group_number', models.CharField(blank=True, max_length=100, null=True)),
                ('coverage_dates', models.DateField(blank=True, null=True)),
                ('contact_information', models.TextField()),
                ('policy_holder_name', models.CharField(blank=True, max_length=100, null=True)),
                ('policy_holder_relationship', models.CharField(blank=True, max_length=50, null=True)),
                ('insurance_card_image', models.ImageField(blank=True, null=True, upload_to='insurance_cards/')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_insurances', to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='HealthGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_description', models.CharField(max_length=200)),
                ('target_date', models.DateField()),
                ('progress', models.IntegerField(default=0, help_text='Progress in percentage')),
                ('status', models.CharField(choices=[('in_progress', 'In Progress'), ('pending', 'Pending'), ('complete', 'Complete')], default='pending', max_length=20)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_goals', to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='HealthcareProfessional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='default.png', upload_to='healthcare_professionals/%Y/%m/%d/')),
                ('name', models.CharField(max_length=255)),
                ('health_facility', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('working_hours', models.CharField(max_length=255)),
                ('education', models.TextField()),
                ('experience_years', models.PositiveIntegerField()),
                ('certifications', models.TextField()),
                ('services_offered', models.TextField()),
                ('languages_spoken', models.TextField()),
                ('emergency_contact', models.CharField(max_length=15)),
                ('insurance_accepted', models.TextField()),
                ('appointment_booking_info', models.TextField()),
                ('patient_reviews', models.TextField()),
                ('professional_memberships', models.TextField()),
                ('additional_notes', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='healthcare_professionals', to='patientapp.patient')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.healthcarespecialty')),
            ],
            options={
                'verbose_name': 'Healthcare Professional',
                'verbose_name_plural': 'Healthcare Professionals',
            },
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='user_uploads/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('file_details', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_uploads', to='patientapp.additionaluser')),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMedicalHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_condition', models.CharField(max_length=100)),
                ('affected_member_name', models.CharField(max_length=100)),
                ('relationship', models.CharField(max_length=100)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_type', models.CharField(blank=True, max_length=50, null=True)),
                ('exercise_duration', models.IntegerField(blank=True, null=True)),
                ('exercise_frequency', models.CharField(blank=True, max_length=50, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorSpecialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_category', models.CharField(max_length=50, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patientapp.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('date', models.DateField()),
                ('diagnosis', models.TextField()),
                ('duration_on_dialysis', models.CharField(max_length=50)),
                ('current_medication', models.TextField()),
                ('general_status', models.CharField(max_length=50)),
                ('access_site_status', models.CharField(max_length=50)),
                ('bp', models.CharField(max_length=20)),
                ('qb_rate', models.CharField(max_length=20)),
                ('ultrafiltration_volume', models.CharField(max_length=20)),
                ('investigations', models.TextField()),
                ('plan', models.TextField()),
                ('additional_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_notes', to='patientapp.additionaluser')),
            ],
        ),
        migrations.CreateModel(
            name='Dietary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dietary_preferences', models.CharField(blank=True, max_length=50, null=True)),
                ('food_allergies', models.CharField(blank=True, max_length=100, null=True)),
                ('balanced_diet', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentMedication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=100)),
                ('reason', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=50, null=True)),
                ('time_from', models.CharField(max_length=50, null=True)),
                ('time_to', models.CharField(max_length=50, null=True)),
                ('from_to', models.CharField(max_length=50, null=True)),
                ('appointment_date', models.DateField(null=True)),
                ('month', models.CharField(max_length=50, null=True)),
                ('date', models.CharField(max_length=50, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patientapp.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField(null=True)),
                ('appointment_status', models.BooleanField(default='inactive')),
                ('booking_date', models.DateField(null=True)),
                ('followup_date', models.DateField(null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patientapp.patient')),
            ],
        ),
        migrations.AddField(
            model_name='allergy',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient'),
        ),
        migrations.CreateModel(
            name='Alcohol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alcohol_consumption', models.BooleanField(default=False)),
                ('alcohol_frequency', models.CharField(blank=True, max_length=20, null=True)),
                ('alcohol_types', models.CharField(blank=True, max_length=100, null=True)),
                ('alcohol_units_per_week', models.IntegerField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patientapp.patient')),
            ],
        ),
    ]
