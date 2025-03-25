from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import HealthRecord
import joblib
import pandas as pd
import os
import numpy as np

# Load the model and scaler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
model = joblib.load(os.path.join(BASE_DIR, "models", "cardio_model.pkl"))

def health_form(request):
    if request.method == "POST":
        try:
            # Extract and convert form data properly
            name = request.POST.get("name")
            age = int(request.POST.get("age"))
            gender = 1 if request.POST.get("gender").lower() == "male" else 0
            height = int(request.POST.get("height"))
            weight = int(request.POST.get("weight"))
            systolic = int(request.POST.get("systolic"))
            diastolic = int(request.POST.get("diastolic"))
            cholesterol = int(request.POST.get("cholesterol"))
            glucose = int(request.POST.get("glucose"))

            # Save the data to the database
            health_record = HealthRecord.objects.create(
                name=name,
                age=age,
                gender=gender,
                height=height,
                weight=weight,
                systolic=systolic,
                diastolic=diastolic,
                cholesterol=cholesterol,
                glucose=glucose,
            )

            # Prepare the input data for the model
            new_user = {
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "ap_hi": systolic,
                "ap_lo": diastolic,
                "cholesterol": cholesterol,
                "gluc": glucose,
                "smoke": 0,
                "alco": 0,
                "active" : 1
            }

            # Convert to DataFrame and scale the data
            new_user_df = pd.DataFrame([new_user])
            new_user_scaled = scaler.transform(new_user_df)

            # Get the probability prediction
            prediction = model.predict(np.array(new_user_scaled))[0][0]
            probability_percent = int(prediction * 100)

            return redirect(f"/dashboard?name={name}&age={age}&gender={gender}&height={height}&weight={weight}&systolic={systolic}&diastolic={diastolic}&cholesterol={cholesterol}&glucose={glucose}&probability={probability_percent}")

        except ValueError as e:
            return JsonResponse({"success": False, "message": f"Invalid input: {e}"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Something went wrong: {e}"})

    return render(request, "health_form.html")


def dashboard(request):
    try:
        probability = int(request.GET.get("probability", 0))
    except ValueError:
        probability = 0
    context = {
        "name": request.GET.get("name", "N/A"),
        "age": request.GET.get("age", "N/A"),
        "gender": "Male" if request.GET.get("gender", "0") == "1" else "Female",
        "height": request.GET.get("height", "N/A"),
        "weight": request.GET.get("weight", "N/A"),
        "systolic": request.GET.get("systolic", "N/A"),
        "diastolic": request.GET.get("diastolic", "N/A"),
        "cholesterol": request.GET.get("cholesterol", "N/A"),
        "glucose": request.GET.get("glucose", "N/A"),
        "probability": probability
    }
    return render(request, "dashboard.html", context)
