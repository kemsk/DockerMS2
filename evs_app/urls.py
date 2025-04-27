from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-violation/', views.add_violation, name='add_violation'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('ticket/<str:ticket_id>/', views.ticket_details, name='ticket_details'),
    path('update-violation-status/', views.update_violation_status, name='update_violation_status'),
]
