from django.db import models

# Create your models here.
class StudentDirectory(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    course = models.CharField(max_length=200)
    year_level = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    school_year = models.CharField(max_length=200, blank=True, null=True)
    college = models.CharField(max_length=200, blank=True, null=True)
    photo = models.FileField(upload_to='student_photos/', blank=True, null=True)