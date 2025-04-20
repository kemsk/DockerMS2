from django.urls import path
from . import views

urlpatterns = [
    path('get_student_info/', views.get_student_info, name='get_student_info'),
]