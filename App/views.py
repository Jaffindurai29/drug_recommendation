from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

import pandas as pd
import random

import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

import random
import pandas as pd
import numpy as np
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

# Create DataFrame
df = pd.DataFrame(data)

# Encode categorical data with separate LabelEncoders for each column
encoders = {col: LabelEncoder() for col in df.columns}
for col in df.columns:
    df[col] = encoders[col].fit_transform(df[col])

# Split dataset
X = df.drop(columns=["disease"])  # Features
y = df["disease"]  # Target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Function to predict disease
def predict_disease(user_input):
    try:
        user_data = np.array([[encoders[col].transform([user_input[col]])[0] for col in X.columns]])
        prediction = model.predict(user_data)
        return encoders["disease"].inverse_transform(prediction)[0]
    except ValueError:
        return "Invalid input! Make sure you are entering correct values."

# Example user input (Modify as needed)
user_input = {
    "symptom": "fever",
    "duration": "5",
    "age": "25",
    "medication": "none",
    "travel": "no",
    "family_history": "no",
    "lifestyle": "healthy"
}

# Predict disease
predicted_disease = predict_disease(user_input)
print(f"Predicted Disease: {predicted_disease}")

# Create your views here.
def home(request):
    return render(request,'management.html',{})

def index(request):
    return render(request,'index.html',{})

from django.shortcuts import render, redirect
from .forms import PatientForm, AppointmentForm, FeedbackForm
from .models import Patient, Appointment, Feedback


# Register Patient
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
    if request.method == 'POST':
        symptom = request.POST['symptoms'].lower()
        doctor_map = {
            'fever': ('Dr. A Kumar', 'General Physician'),
            'skin': ('Dr. B Mehta', 'Dermatologist'),
            'heart': ('Dr. C Patel', 'Cardiologist'),
            'sugar': ('Dr. D Iyer', 'Endocrinologist'),
            'lungs': ('Dr. E Reddy', 'Pulmonologist'),
            'kidney': ('Dr. F Singh', 'Nephrologist'),
            'pregnancy': ('Dr. G Das', 'Gynecologist'),
            'pain': ('Dr. H Shah', 'Orthopedic'),
            'mental': ('Dr. I Varma', 'Psychiatrist'),
            'infection': ('Dr. J Nair', 'Infectious Disease Specialist')
        }
        for key in doctor_map:
            if key in symptom:
                suggested_doctors.append(doctor_map[key])
    return render(request, 'doctor_suggestion.html', {'suggested_doctors': suggested_doctors})


from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("disease_data.csv")

# Encode categorical data
encoder = LabelEncoder()
for col in df.columns[:-1]:  
    df[col] = encoder.fit_transform(df[col])

df["disease"] = encoder.fit_transform(df["disease"])

# Train Random Forest Model
X = df.drop(columns=["disease"])
y = df["disease"]
model = RandomForestClassifier()
model.fit(X, y)

def drug_recommendation(request):
    if request.method == "POST":
        user_input = {
            "symptom": request.POST.get("symptom"),
            "duration": request.POST.get("duration"),
            "age": request.POST.get("age"),
            "medication": request.POST.get("medication"),
            "travel": request.POST.get("travel"),
            "family_history": request.POST.get("family_history"),
            "lifestyle": request.POST.get("lifestyle"),
        }
        

        # Convert input to model format
        try:
           print(user_input,user_input)
           predicted_disease = predict_disease(user_input)
           print(f"Predicted Disease: {predicted_disease}")    
            
        except Exception as e:
            print(e)
            predicted_disease = "Unknown disease"

        # Drug recommendations (example)
        drug_dict = {
            "cold": ["Paracetamol", "Antihistamines"],
            "flu": ["Tamiflu", "Ibuprofen"],
            "asthma": ["Salbutamol", "Inhalers"],
            "dengue": ["Hydration", "Paracetamol"],
            "diabetes": ["Metformin", "Insulin"],
        }
        
        recommended_drugs = drug_dict.get(predicted_disease, ["Consult a doctor"])
        food = 'Soft foods, avoid spicy items'
        return render(request, 'drug_recommendation.html', {'recommendation': recommended_drugs, 'food': food})

        return render(request, "results.html", {"disease": predicted_disease, "drugs": recommended_drugs})

    return render(request, "drug_recommendation.html")

# Predict disease
    predicted_disease = predict_disease(user_input)
    recommendation, food = '', ''
    if request.method == 'POST':
        symptom = request.POST['symptom'].lower()
        if 'fever' in symptom:
            recommendation = 'Paracetamol'
            food = 'Hot soup, plenty of fluids'
        elif 'cough' in symptom:
            recommendation = 'Cough Syrup'
            food = 'Warm tea, honey'
        elif 'pain' in symptom:
            recommendation = 'Ibuprofen'
            food = 'Soft foods, avoid spicy items'
    return render(request, 'drug_recommendation.html', {'recommendation': recommendation, 'food': food})


def audio_call(request):
    return render(request,'audio_call.html')  

def video_call(request):
    return render(request,'video_call.html')  



def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username,password=password,email=email)
        return redirect('login')
    return render(request,"signup.html",{})  

def app_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password) 
        if user is not None:
            login(request,user)

            return redirect('management')
    return render(request,"login.html",{})

   
