from django.db import models

class Student(models.Model):
    studentId = models.CharField(max_length=20, primary_key=True)
    fullName = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    yearLevel = models.CharField(max_length=10)
    email = models.EmailField()
    contactNumber = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    class Meta:
        app_label = 'AD_EVS'
        db_table = 'students'
