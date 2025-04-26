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
