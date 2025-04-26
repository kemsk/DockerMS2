from django.shortcuts import render
from datetime import datetime
from .models import Violation  # Import your model

def dashboard_view(request):
    now = datetime.now()

    violations = Violation.objects.all()  # Fetch all violations

    context = {
        'violations': violations,
        'current_day': now.strftime('%A'),       # Day: Monday, Tuesday, etc.
        'current_month': now.strftime('%B'),     # Month: April, May, etc.
        'current_date': now.strftime('%d'),      # Date: 24
        'current_time': now.strftime('%I:%M:%S %p'), # Time: 02:30:00 PM 
        'current_year': now.strftime('%Y'),      # Year: 2025
    }

    return render(request, 'dashboard.html', context)

