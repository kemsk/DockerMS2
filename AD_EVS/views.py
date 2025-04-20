from django.shortcuts import render
from .models import Student

def get_student_info(request):
    student_info = None
    
    if request.method == "GET":
        student_id = request.GET.get('studentId')  # Get studentId from the query parameters
        if student_id:
            try:
                # Attempt to retrieve the student based on studentId
                student_info = Student.objects.get(studentId=student_id)
            except Student.DoesNotExist:
                student_info = None  # If no student is found with the given ID
    
    # Render the HTML page with the student information (if found)
    return render(request, 'student_info.html', {'student_info': student_info})
