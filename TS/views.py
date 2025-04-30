from django.shortcuts import render
from datetime import datetime
from .models import * 

def dashboard_view(request):
    return render(request, 'system/dashboard.html')

def add_violation(request):
    return render(request, 'system/addViolation.html')

def user_management_view(request):
    return render(request, 'system/manageUsers.html')