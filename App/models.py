from django.db import models
import random

def generate_unique_token():
    from App.models import Patient
    while True:
        token = str(random.randint(100, 999))  # Generates 3-digit number as string
        if not Patient.objects.filter(token=token).exists():
            return token

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15)
    token = models.CharField(max_length=3, unique=True, default=generate_unique_token)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

class Feedback(models.Model):
    patient = models.CharField(max_length=100)
    rating = models.IntegerField()
    message = models.TextField()
