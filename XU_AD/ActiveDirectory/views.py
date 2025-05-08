from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StudentDirectory
import os
import jwt
import json

# Token decoder utility
def token_decoder(token):
    secret_key = os.environ.get('SECRET_KEY')
    return jwt.decode(token, secret_key, algorithms=['HS256'])

def test_connection(request):
    return JsonResponse({'message': "Connected"}, status=200)

@csrf_exempt
def student_view(request):
    # Add logging for debugging
    print(f"Received request method: {request.method}")
    print(f"GET parameters: {request.GET}")
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            data = body.get('data', [])
            for student in data:
                if not StudentDirectory.objects.filter(student_id=student['student_id']).exists():
                    StudentDirectory.objects.create(
                        student_id=student.get('student_id'),
                        first_name=student.get('first_name'),
                        last_name=student.get('last_name'),
                        middle_name=student.get('middle_name'),
                        course=student.get('course'),
                        year_level=student.get('year_level'),
                        phone_number=student.get('phone_number'),
                        address=student.get('address'),
                        emergency_contact_number=student.get('emergency_contact_number'),
                        emergency_contact_name=student.get('emergency_contact_name'),
                        birthdate=student.get('birthdate'),
                        school_year=student.get('school_year'),
                        college=student.get('college'),
                        photo=student.get('photo') if isinstance(student.get('photo'), str) else None,
                    )
            return JsonResponse({'message': 'Students saved successfully.', 'success': True})
        except Exception as e:
            return JsonResponse({'message': str(e), 'success': False}, status=400)

    elif request.method == "GET":
        try:
            filters = {}
            student_id = request.GET.get('student_id')
            first_name = request.GET.get('first_name')
            last_name = request.GET.get('last_name')
            middle_name = request.GET.get('middle_name')

            if student_id:
                filters['student_id'] = student_id
            if first_name:
                filters['first_name__icontains'] = first_name
            if last_name:
                filters['last_name__icontains'] = last_name
            if middle_name:
                filters['middle_name__icontains'] = middle_name

            # Log the filters being used for search
            print(f"Search filters: {filters}")
            students = list(StudentDirectory.objects.filter(**filters).values())
            print(f"Found {len(students)} students")
            return JsonResponse({'students': students, 'success': True})
        except Exception as e:
            return JsonResponse({'message': str(e), 'success': False}, status=500)

    elif request.method == "DELETE":
        try:
            body = json.loads(request.body)
            delete_all = body.get('delete_all', False)
            student_id = body.get('student_id')

            if delete_all:
                count, _ = StudentDirectory.objects.all().delete()
                return JsonResponse({'message': f'All {count} students deleted.', 'success': True})
            elif student_id:
                deleted, _ = StudentDirectory.objects.filter(student_id=student_id).delete()
                if deleted:
                    return JsonResponse({'message': 'Student deleted successfully.', 'success': True})
                else:
                    return JsonResponse({'message': 'Student not found.', 'success': False}, status=404)
            else:
                return JsonResponse({'message': 'Provide either "student_id" or "delete_all": true', 'success': False}, status=400)

        except Exception as e:
            return JsonResponse({'message': str(e), 'success': False}, status=400)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)
