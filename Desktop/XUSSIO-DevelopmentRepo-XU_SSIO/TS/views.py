from django.shortcuts import render
from datetime import datetime
from .models import * 

def dashboard_view(request):
    now = datetime.now()

    violations = Violation.objects.all()  # Fetch all violations

    context = {
        'violations': violations,
    }

    return render(request, 'system/dashboard.html', context)

def add_violation(request):
    return render(request, 'system/addViolation.html')

def manage_users(request):
    return render(request, 'system/manageUsers.html')

def ticket_details(request, ticket_id):
    return render(request, 'system/ticketDetails.html', {'ticket_id': ticket_id})

def edit_violation(request, violation_id):
    return render(request, 'system/editViolation.html', {'violation_id': violation_id})

def delete_violation(request, violation_id):
    return render(request, 'system/deleteViolation.html', {'violation_id': violation_id})




