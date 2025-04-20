<<<<<<< HEAD
from django.db import models

class Student(models.Model):
=======
# app/models_activedirectory.py
from django.db import models

class ADStudent(models.Model):
>>>>>>> f1d7af53b2ec1c899a873523aef130c85bdfcbd5
    studentId = models.CharField(max_length=20, primary_key=True)
    fullName = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    yearLevel = models.CharField(max_length=10)
    email = models.EmailField()
<<<<<<< HEAD
    contactNumber = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    class Meta:
        app_label = 'AD_EVS'
        db_table = 'students'
=======
    contactNumber = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False  # Django won't try to create tables
        db_table = 'students'
        app_label = 'your_app_name'
>>>>>>> f1d7af53b2ec1c899a873523aef130c85bdfcbd5
