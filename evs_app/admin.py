from django.contrib import admin
from .models import Violation, Reason, ViolationRecord, SSIOMember, Student

@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(ViolationRecord)
class ViolationRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'student', 'violation', 'date_recorded', 'is_resolved')
    list_filter = ('is_resolved', 'violation', 'date_recorded')
    search_fields = ('student__name', 'student__student_id')
    date_hierarchy = 'date_recorded'

@admin.register(SSIOMember)
class SSIOMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id')
    search_fields = ('name', 'student_id')
