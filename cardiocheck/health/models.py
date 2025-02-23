from django.db import models

class HealthRecord(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    ACTIVITY_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)  # in cm
    weight = models.PositiveIntegerField(null=True, blank=True)  # in kg
    systolic = models.PositiveIntegerField(null=True, blank=True)  # BP upper value
    diastolic = models.PositiveIntegerField(null=True, blank=True)  # BP lower value
    cholesterol = models.PositiveIntegerField(null=True, blank=True)
    glucose = models.PositiveIntegerField(null=True, blank=True)
    activity = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.age} years"
