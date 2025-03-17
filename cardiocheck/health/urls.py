from django.urls import path
from .views import *

urlpatterns = [
    path('', health_form, name="health_form"),
    path('dashboard', dashboard, name="dashboard"),

]
