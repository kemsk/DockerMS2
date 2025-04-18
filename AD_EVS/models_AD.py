# app/models_activedirectory.py
from django.db import models

class ADStudent(models.Model):
    studentId = models.CharField(max_length=20, primary_key=True)
    fullName = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    yearLevel = models.CharField(max_length=10)
    email = models.EmailField()
    contactNumber = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False  # Django won't try to create tables
        db_table = 'students'
        app_label = 'your_app_name'
