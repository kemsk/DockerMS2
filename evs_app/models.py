from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Violation(models.Model):
    """Model for violation types (e.g., ID Violation, Dress Code Violation)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Reason(models.Model):
    """Model for reasons within violation types (e.g., 'No ID', 'Improper Uniform')"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    """Model for student information"""
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.student_id})"

class SSIOMember(models.Model):
    """Extended user model for SSIO staff members"""
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('encoder', 'Encoder'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='encoder')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"

class ViolationRecord(models.Model):
    """Model for entry violation records"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('claimed', 'ID Claimed'),
        ('resolved', 'Resolved'),
    )
    
    record_id = models.AutoField(primary_key=True)
    ticket_number = models.CharField(max_length=20, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    violation = models.ForeignKey(Violation, on_delete=models.CASCADE)
    reason = models.ForeignKey(Reason, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    photo_proof = models.ImageField(upload_to='violations/', null=True, blank=True)
    
    date_recorded = models.DateTimeField(default=timezone.now)
    recorded_by = models.ForeignKey(SSIOMember, on_delete=models.SET_NULL, null=True, related_name='recorded_violations')
    
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(SSIOMember, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_violations')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.student.name}"
    
    def resolve(self, ssio_member):
        """Mark violation as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.resolved_by = ssio_member
        self.status = 'resolved'
        self.save()
    
    def mark_claimed(self):
        """Mark ID as claimed"""
        self.status = 'claimed'
        self.save()
