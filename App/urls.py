from django.urls import path
from . views import *

urlpatterns = [
    path('home/',home,name='management'),
    path('index/',index,name='index'),
    path('register/',register_patient, name='register_patient'),
    path('patients/',view_patients, name='view_patients'),
    path('book_appointment/',book_appointment, name='book_appointment'),
    path('success/',appointment_success, name='appointment_success'),
    path('appointments/',view_appointments, name='view_appointments'),
    path('feedback/',feedback, name='feedback'),
    path('doctor_suggestion/',doctor_suggestion, name='doctor_suggestion'),
    path('drug/',drug_recommendation, name='drug_recommendation'),
    path('audio_call_page/',audio_call, name='audio_call'),
    path('video_call_page/', video_call, name='video_call'),
    path('',app_login,name='login'),
    path('signup/',signup,name="signup"),
 ]