from django.urls import path
from . import views

app_name = 'ts'

urlpatterns = [
    path('dashboard', views.dashboard_view, name='Dashboard'),
    path('add-violation', views.add_violation, name="AddViolation"),
    path('user-management', views.user_management_view, name="UserManagement")
]