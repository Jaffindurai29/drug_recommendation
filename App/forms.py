from django import forms
from .models import Patient, Appointment, Feedback

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
