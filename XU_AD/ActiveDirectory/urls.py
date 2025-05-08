from django.urls import path
from . import views 
urlpatterns = [
    path('student', views.student_view),
    path('test-connection', views.test_connection)
]