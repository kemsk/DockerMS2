from django.db import models

# Create your models here.

class Violation(models.Model):
    student_name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=20)
    ticket_number = models.CharField(max_length=10)
    violation_type = models.CharField(max_length=50)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student_name} - {self.violation_type}"
    
    