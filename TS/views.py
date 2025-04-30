from django.shortcuts import render, redirect
from datetime import datetime
from django.core.paginator import Paginator
from .models import * 
import json
from django.db.models import Sum, Q, Count
from django.http import JsonResponse, HttpResponseNotAllowed

def paginate_queryset(request, queryset, per_page):
    page_number = request.GET.get('page')
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)

def active_list():
    ay = AcademicYear.objects.filter(active=1)
    return ay

def dashboard_view(request):
    ay_id = active_list()

    student_name = request.GET.get('student_name', '')
    student_id = request.GET.get('student_id', '')
    filter_date = request.GET.get('filter_date', '')

    tickets = Ticket.objects.filter(acad_year__in=ay_id)

    if student_name:
        name_terms = student_name.split()
        for term in name_terms:
            tickets = tickets.filter(
                Q(student__first_name__icontains=term) |
                Q(student__middle_name__icontains=term) |
                Q(student__last_name__icontains=term)
            )

    if student_id:
        tickets = tickets.filter(student__student_id__icontains=student_id)

    if filter_date:
        try:
            date_obj = datetime.strptime(filter_date, "%Y-%m-%d").date()
            tickets = tickets.filter(date_created__date=date_obj)
        except ValueError:
            pass

    tickets = tickets.order_by('-ticket_id')
    page_obj = paginate_queryset(request, tickets, 10)

    context = {
        'tickets': page_obj,
    }
    return render(request, 'system/dashboard.html', context)

def add_violation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # parse raw JSON

            ay_id = AcademicYear.objects.get(active=1)

            ticket_id = data.get('ticket_id')
            violations = data.get('violations', [])
            remarks = data.get('remarks')
            student_id = data.get('student_id')

            id_violation = 'id_violation' in violations
            dress_code_violation = 'dress_code_violation' in violations
            uniform_violation = 'uniform_violation' in violations

            Ticket.objects.create(
                ticket_id=ticket_id,
                uniform_violation=uniform_violation,
                dress_code_violation=dress_code_violation,
                id_violation=id_violation,
                ssio_id=1,  #CHANGE UPON AD AND USER INTEGRATION
                id_status=0,
                ticket_status=0,
                remarks=remarks,
                student_id=student_id,
                acad_year=ay_id.acad_year_id,
                photo_path="",
                date_created=datetime.now(),
                date_validated=None,
                semester=ay_id.semester,
            )

            return JsonResponse({'message': 'Violation added successfully', 'success':True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    last_ticket = Ticket.objects.order_by('-ticket_id').first()
    new_ticket_id = last_ticket.ticket_id + 1

    violations = Violation.objects.all()

    return render(request, 'system/addViolation.html', {
        'ticket_id': new_ticket_id,
        'violations': violations
    })
    

def user_management_view(request):
    return render(request, 'system/manageUsers.html')

def ticket_details_view(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    student = Student.objects.get(student_id=ticket.student.student_id)
    violations = Violation.objects.all()

    ## ADD AUTO RETRIEVAL OF PHOTO 

    return render(request, 'system/ticket-details.html', {
        'ticket': ticket,
        'student': student,
        'violations': violations
    })

def update_id_status(request, ticket_id):
    if request.method == 'POST':
        try:
            content_type = request.META.get('CONTENT_TYPE', '')

            if 'application/json' in content_type:
                data = json.loads(request.body)
                new_status = data.get('status')
            else:
                new_status = request.POST.get('status')

            ticket = Ticket.objects.get(ticket_id=ticket_id)
            ticket.id_status = new_status
            ticket.save()

            if 'application/json' in content_type:
                return JsonResponse({'message': 'ID Status updated successfully'})
            else:
                return redirect('ts:Dashboard')
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return redirect('ts:Dashboard')