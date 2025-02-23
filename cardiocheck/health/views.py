from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import HealthRecord

def health_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        systolic = request.POST.get("systolic")
        diastolic = request.POST.get("diastolic")
        cholesterol = request.POST.get("cholesterol")
        glucose = request.POST.get("glucose")
        activity = request.POST.get("activity")

        # Save to database
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
            activity=activity,
        )

        return redirect("dashboard")

    return render(request, "health_form.html")

def dashboard(request):
    return render(request, "dashboard.html")
