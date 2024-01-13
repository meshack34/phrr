from django.urls import path
from .import views 
urlpatterns = [
    # new
    path('',views.home, name='home'),
    path('patient_register/',views.patient_register, name='register'),
    path('login/',views.user_login, name='login'),
    # path('upload-file/<int:user_id>/<str:file_type>/', views.upload_file, name='upload_file'),
      path('view-file/<int:file_upload_id>/', views.view_file, name='view_file'),

    
    path('patient/dashboard/',views.patient_dashboard, name='patient_dashboard'),
    path('patients_profile/', views.patients_profile, name='patients_profile'),
    path('recover_account_id/', views.recover_account_id, name='recover_account_id'),
    path('account_recovery/', views.account_recovery, name='account_recovery'),    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:email_b64>/<str:token>/', views.reset_password, name='reset_password'),
    
    path('create_additional_user/', views.create_additional_user, name='create_additional_user'),
    path('display_additional_users/', views.display_additional_users, name='display_additional_users'),
    
    path('discharge-form/', views.discharge_form, name='discharge_form'),

  
 
    path('view_nursing_notes/<pk>', views.view_nursing_notes,  name='view_nursing_notes'),
    
    path('view_nursing_notes/<int:additional_user_id>/', views.view_nursing_notes, name='view_nursing_notes'),
    path('doctor_note_form/<int:additional_user_id>/', views.doctor_note_form, name='doctor_note_form'),
    path('user_details/<int:additional_user_id>/', views.user_details, name='user_details'),
  
    # path('upload_file/<int:additional_user_id>/<str:file_type>/', views.upload_file, name='upload_file'),
   
    path('download_file/<int:additional_user_id>/<str:file_type>/', views.download_file, name='download_file'),
    path('upload_file/<int:additional_user_id>/', views.upload_file, name='upload_file'),
    
    
    path('toggle_active/<str:additional_user_id>/', views.toggle_active, name='toggle_active'),

   

    path('manage_emergency_contact/', views.manage_emergency_contact, name='manage_emergency_contact'),
    
    path('add/', views.add_healthcare_speciality, name='add_healthcare_speciality'),
    path('update/<int:pk>/', views.update_healthcare_speciality, name='update_healthcare_speciality'),
    path('delete/<int:pk>/', views.delete_healthcare_speciality, name='delete_healthcare_speciality'),

  
  # urls.py
    path('add_healthcare_professional/', views.add_healthcare_professional, name='add_healthcare_professional'),
    path('healthcare_professionals/', views.healthcare_professionals, name='healthcare_professionals'),

    # path('add_health_insurance/', views.add_health_insurance, name='add_health_insurance'),
    # path('view_health_insurance/', views.view_health_insurance, name='view_health_insurance'),
    path('add_health_insurance/', views.add_health_insurance, name='add_health_insurance'),
    path('health_insurance_list/', views.health_insurance_list, name='health_insurance_list'),
    
    
    # Your existing URLs

    path('add_vitals/', views.add_vitals, name='add_vitals'),
    path('view_vitals/', views.view_vitals, name='view_vitals'),
    path('update_vitals/<int:vitals_id>/', views.update_vitals, name='update_vitals'),
    path('delete_vitals/<int:vitals_id>/', views.delete_vitals, name='delete_vitals'),
    path('print/<int:vitals_id>/', views.print_vitals_pdf, name='print_vitals_pdf'),
    path('newadd_medical_history/', views.newadd_medical_history, name='newadd_medical_history'),
    path('newview_medical_history/', views.newview_medical_history, name='newview_medical_history'),    
    path('update_medical_history/<int:record_id>/', views.update_medical_history, name='update_medical_history'),
    path('add_lifestyle_details/', views.add_lifestyle_details, name='add_lifestyle_details'),
    path('view_lifestyle_details/', views.view_lifestyle_details, name='view_lifestyle_details'),
    path('add_medical_history/',  views.add_medical_history, name='add_medical_history'),
    path('view_medical_history/', views.view_medical_history, name='view_medical_history'),
    path('update_medical_history/<int:medical_history_id>/',  views.update_medical_history, name='update_medical_history'),
    path('delete_medical_history/<int:medical_history_id>/',  views.delete_medical_history, name='delete_medical_history'),
    path('print_medical_history_pdf/<int:medical_history_id>/',  views.print_medical_history_pdf, name='print_medical_history_pdf'),
    path('add_treatment_record/',  views.add_treatment_record, name='add_treatment_record'),
    path('view_treatment_records/',  views.view_treatment_records, name='view_treatment_records'),
    path('update_treatment_record/<int:treatment_record_id>/',  views.update_treatment_record, name='update_treatment_record'),
    path('delete_treatment_record/<int:treatment_record_id>/',  views.delete_treatment_record, name='delete_treatment_record'),
    path('print_treatment_record_pdf/<int:treatment_record_id>/',  views.print_treatment_record_pdf, name='print_treatment_record_pdf'),
   
    path('add_health_goal/', views.add_health_goal, name='add_health_goal'),
    path('health_goal_list/', views.health_goal_list, name='health_goal_list'),
   
     #complete order urls
    
   

    path('profile/<int:doctor_id>/', views.profile, name='profile'),
    
    path('patient_appointment/<int:doctor_id>/', views.patient_appointment, name='patient_appointment'),
    path('appointments/', views.appointments, name="appointments"),
    path('doctor_search/', views.doctor_search, name='doctor_search'),
    path('doctors/',views.doctors, name='doctors'),
    path('booking/<int:doctor_id>/', views.booking, name='booking'),
    path('history/', views.history, name='history'),
    path('view_history/<int:patient_id>/', views.view_history, name='view_history'),
    
    path('doctor/register/',views.doc_register, name='doctor-register'),
   
    path('logout/',views.logout, name='logout'),
    path('doctor/dashboard/',views.doctor_dashboard, name='doctor_dashboard'),
    path('status/<int:patient_id>',views.status, name='status'),
    path('current/patient/<int:patient_id>/', views.current_patient, name="current_patient"),
    path('Prescription/<int:patient_id>/', views.getPrescriptionForDoc, name="getPrescriptionForDoc"),
    path('treatmentpdf/<int:patient_id>/', views.generate_medical_treatment_pdf, name="generatedpdf"),
    path('lab-report/<int:patient_id>/', views.lab_report, name='lab_report'),
    path('lab-report-confirmation/<int:lab_report_id>/', views.lab_report_confirmation, name='lab_report_confirmation'),
    path('treatment/<int:patient_id>/', views.Medication, name='patient-medicals'),
     path('view_medical_history/<int:patient_id>/', views.view_medical_history, name='view_medical_history'),
    path('doctor-profile/',views.doctor_profile, name='doctor_profile'),
    path('doctor_specialization/',views.doctor_specialization, name='doctor_specialization'),
    
    path('medical_history/', views.medical_history, name='medical_history'),
    path('schedule_timing/<int:doctor_id>/', views.schedule_timing, name='schedule_timing'),
    path('mypatients', views.mypatients, name='mypatients'),
    path('viewReview/', views.viewReview, name="viewReview"),
    path('viewReviewOnProfile/', views.viewReviewOnProfile, name="viewReviewOnProfile"),
    
]
