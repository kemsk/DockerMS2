from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
import json
import uuid

from .models import Violation, Reason, ViolationRecord, SSIOMember, Student
from .forms import LoginForm, ViolationRecordForm, SSIOMemberForm, StudentForm

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'evs_app/login.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    """Display the main dashboard with violation records"""
    violations = ViolationRecord.objects.all().order_by('-date_recorded')
    
    context = {
        'violations': violations,
        'current_user': request.user
    }
    return render(request, 'evs_app/dashboard.html', context)

@login_required
def add_violation(request):
    """Add a new violation record"""
    if request.method == 'POST':
        form = ViolationRecordForm(request.POST, request.FILES)
        student_form = StudentForm(request.POST)
        
        if form.is_valid() and student_form.is_valid():
            # Get or create the student
            student_name = student_form.cleaned_data['name']
            student_id = student_form.cleaned_data['student_id']
            
            student, created = Student.objects.get_or_create(
                student_id=student_id,
                defaults={'name': student_name}
            )
            
            # Create the violation record
            violation_record = form.save(commit=False)
            violation_record.student = student
            
            # Generate a ticket number
            current_year = timezone.now().year
            random_suffix = uuid.uuid4().hex[:6]
            ticket_number = f"{current_year}-{random_suffix}"
            violation_record.ticket_number = ticket_number
            
            # Set the recorder
            try:
                ssio_member = SSIOMember.objects.get(user=request.user)
                violation_record.recorded_by = ssio_member
            except SSIOMember.DoesNotExist:
                pass  # Handle case where the user is not an SSIO member
            
            violation_record.save()
            messages.success(request, f'Violation record created with ticket number {ticket_number}')
            return redirect('dashboard')
    else:
        form = ViolationRecordForm()
        student_form = StudentForm()
    
    violations = Violation.objects.all()
    context = {
        'form': form,
        'student_form': student_form,
        'violations': violations,
        'current_user': request.user
    }
    return render(request, 'evs_app/add_violation.html', context)

@login_required
def manage_users(request):
    """Manage SSIO users"""
    users = SSIOMember.objects.all()
    
    if request.method == 'POST':
        form = SSIOMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('manage_users')
    else:
        form = SSIOMemberForm()
    
    context = {
        'users': users,
        'form': form,
        'current_user': request.user
    }
    return render(request, 'evs_app/manage_users.html', context)

@login_required
def ticket_details(request, ticket_id):
    """View details of a specific violation record"""
    violation = get_object_or_404(ViolationRecord, ticket_number=ticket_id)
    
    context = {
        'violation': violation,
        'current_user': request.user
    }
    return render(request, 'evs_app/ticket_details.html', context)

@login_required
def update_violation_status(request):
    """AJAX endpoint to update violation status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            violation_id = data.get('violation_id')
            status = data.get('status')
            
            violation = get_object_or_404(ViolationRecord, record_id=violation_id)
            
            if status == 'claimed':
                violation.mark_claimed()
            elif status == 'resolved':
                try:
                    ssio_member = SSIOMember.objects.get(user=request.user)
                    violation.resolve(ssio_member)
                except SSIOMember.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'User is not an SSIO member'})
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
