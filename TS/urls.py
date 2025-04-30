from django.urls import path
from . import views

app_name = 'ts'

urlpatterns = [
    path('dashboard', views.dashboard_view, name='Dashboard'),
]