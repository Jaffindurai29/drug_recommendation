from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User


import random

import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Generate synthetic data
symptoms = ["fever", "cough", "fatigue", "body pain", "sore throat", "chills", "headache", "night sweats"]
durations = [str(i) for i in range(1, 15)]
ages = [str(i) for i in range(5, 80)]
medications = ["none", "antibiotics", "inhaler", "pain relievers"]
travel_histories = ["yes", "no"]
family_histories = ["yes", "no"]
lifestyles = ["healthy", "smoking", "poor diet", "active"]
diseases = ["fever", "flu", "asthma", "dengue", "diabetes"]

data = []
for _ in range(100):
    row = {
        "symptom": random.choice(symptoms),
        "duration": random.choice(durations),
        "age": random.choice(ages),
        "medication": random.choice(medications),
        "travel": random.choice(travel_histories),
        "family_history": random.choice(family_histories),
        "lifestyle": random.choice(lifestyles),
        "disease": random.choice(diseases),
    }
    data.append(row)

# Placeholder for the trained model and preprocessor (will be loaded later)
model = None
preprocessor = None

def home(request):
    return render(request,'management.html',{})

def index(request):
    return render(request,'index.html',{})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import PatientForm, AppointmentForm, FeedbackForm
from .models import Patient, Appointment, Feedback
import joblib
import os
import pandas as pd
# Load the trained model and preprocessor
try:
    model = joblib.load('disease_model.pkl')
    preprocessor = joblib.load('preprocessor.pkl')
    model_loaded = True
except (FileNotFoundError, NameError) as e:
    print(f"Error loading model or preprocessor: {e}")
    print("Please run the model training function first.")
    model_loaded = False

# Register Patient
@login_required
def register_patient(request):
    form = PatientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('view_patients')
    return render(request, 'register_patient.html', {'form': form})


# View Patients
def view_patients(request):
    patients = Patient.objects.all()
    return render(request, 'view_patients.html', {'patients': patients})

# Book Appointment
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            print("Appointment saved. Redirecting to success page.")
            return redirect('appointment_success')
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form})


def appointment_success(request):
    return render(request, 'appointment_success.html')

def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'view_appointments.html', {'appointments': appointments})

# Feedback
def feedback(request):
    form = FeedbackForm(request.POST or None)
    feedbacks = Feedback.objects.all()

    if form.is_valid():
        form.save()
        return redirect('feedback')

    # Add stars list to the context
    feedback_data = []
    for fb in feedbacks:
        fb.stars = ['⭐'] * fb.rating  # Create a list with the number of stars based on rating
        feedback_data.append(fb)

    return render(request, 'feedback.html', {'form': form, 'feedbacks': feedback_data})


# Doctor Suggestion
def doctor_suggestion(request):
    suggested_doctors = []
    predicted_disease = "Could not predict disease" # Initialize with a default

    if request.method == 'POST':
        if model_loaded:
            try:
                # Extract user input from the form (adjust keys based on your form)
                user_input = {
                    "symptom": request.POST.get("symptom"),
                    "duration": request.POST.get("duration"),
                    "age": request.POST.get("age"),
                    "medication": request.POST.get("medication"),
                    "travel": request.POST.get("travel"),
                    "family_history": request.POST.get("family_history"),
                    "lifestyle": request.POST.get("lifestyle"),
                }

                # Convert user input to a pandas DataFrame
                user_data = [user_input.get(col) for col in ["symptom", "duration", "age", "medication", "travel", "family_history", "lifestyle"]]
                user_df = pd.DataFrame([user_data], columns=["symptom", "duration", "age", "medication", "travel", "family_history", "lifestyle"])

                # Preprocess user input
                user_processed = preprocessor.transform(user_df)

                # Predict disease
                predicted_disease = model.predict(user_processed)[0]

                # Map predicted disease to specialist and suggested doctors
                doctor_map = {
                    'fever': [('Dr. A Kumar', 'General Physician')],
                    'flu': [('Dr. A Kumar', 'General Physician')],
                    'asthma': [('Dr. E Reddy', 'Pulmonologist')],
                    'dengue': [('Dr. A Kumar', 'General Physician'), ('Dr. J Nair', 'Infectious Disease Specialist')],
                    'diabetes': [('Dr. D Iyer', 'Endocrinologist')],
                    'cold': [('Dr. A Kumar', 'General Physician')],
                    # Add more mappings for other diseases
                }
                suggested_doctors = doctor_map.get(predicted_disease, [('Consult a doctor', 'N/A')])

            except Exception as e:
                print(f"Error during doctor suggestion prediction: {e}")
    return render(request, 'doctor_suggestion.html', {'suggested_doctors': suggested_doctors, 'predicted_disease': predicted_disease})

def drug_recommendation(request):
    recommendation = ''
    food = ''

    if request.method == "POST":
        if model_loaded:
            user_input = {
                "symptom": request.POST.get("symptom"),
                "duration": request.POST.get("duration"),
                "age": request.POST.get("age"),
                "medication": request.POST.get("medication"),
                "travel": request.POST.get("travel"),
                "family_history": request.POST.get("family_history"),
                "lifestyle": request.POST.get("lifestyle"),
            }

            # Convert user input to a format compatible with the preprocessor
            # This assumes the order of columns in user_input matches the training data
            user_data = [user_input.get(col) for col in ["symptom", "duration", "age", "medication", "travel", "family_history", "lifestyle"]]
            user_df = pd.DataFrame([user_data], columns=["symptom", "duration", "age", "medication", "travel", "family_history", "lifestyle"])

            try:
                # Preprocess user input
                user_processed = preprocessor.transform(user_df)

                # Predict disease
                predicted_disease_encoded = model.predict(user_processed)[0]
                # predicted_disease = disease_label_encoder.inverse_transform(predicted_disease_encoded)[0]

                # Since we didn't save the disease label encoder, we'll use a placeholder
                # You should modify this part based on your actual model output and how you handle disease labels
                # For now, let's just use the most frequent disease from the training data as a fallback
                # or have a simple mapping based on the encoded output if possible.
                # A more robust solution would be to save and load the target encoder.
                # Assuming your model directly predicts string labels:
                predicted_disease = predicted_disease_encoded # If model output is string
                # If model output is numerical, you'll need a way to map it back to disease names
                # For now, we'll assume the model outputs the disease name directly or a recognizable ID.

                print(f"Predicted Disease: {predicted_disease}")

            except Exception as e:
                print(f"Error during prediction: {e}")
                predicted_disease = "Could not predict disease"
        else:
            predicted_disease = "Model not loaded. Cannot predict disease."
            print("Model not loaded. Cannot predict disease.")

        # Drug recommendations (example)
        drug_dict = {
            "fever": ["Paracetamol", "Rest"],
            "flu": ["Tamiflu", "Ibuprofen", "Plenty of fluids"],
            "asthma": ["Salbutamol", "Inhalers", "Avoid triggers"],
            "dengue": ["Hydration", "Paracetamol", "Avoid aspirin"],
            "diabetes": ["Metformin", "Insulin", "Diet control"],
            "cold": ["Paracetamol", "Antihistamines", "Rest"],
        }

        recommended_drugs = drug_dict.get(predicted_disease, ["Consult a doctor"])

        # Food suggestions (example)
        food_dict = {
            "fever": "Hot soup, plenty of fluids",
            "flu": "Warm tea, honey, easily digestible food",
            "asthma": "Balanced diet, avoid food triggers",
            "dengue": "Soft foods, plenty of fluids",
            "diabetes": "Low sugar and balanced diet",
            "cold": "Warm tea, honey, chicken soup",
        }
        food = food_dict.get(predicted_disease, "Balanced diet")


        return render(request, 'drug_recommendation.html', {'recommendation': recommended_drugs, 'food': food, 'predicted_disease': predicted_disease})


    return render(request, "drug_recommendation.html")


def audio_call(request):
    return render(request,'audio_call.html')

def video_call(request):
    return render(request,'video_call.html')




def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username,password=password,email=email)
        return redirect('login')
    return render(request,"signup.html",{})

def app_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('management')
        else:
            # You might want to add an error message for invalid credentials
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request,"login.html",{})

def app_logout(request):
    logout(request)
    return redirect('login')