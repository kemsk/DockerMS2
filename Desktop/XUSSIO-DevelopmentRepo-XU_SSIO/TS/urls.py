from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add_violation, name='add_violation'),
    path('manage/', views.manage_users, name='manage_users'),
    path('ticket/<int:ticket_id>/', views.ticket_details, name='ticket_details'),
    path('violation/<int:violation_id>/edit/', views.edit_violation, name='edit_violation'),
    path('violation/<int:violation_id>/delete/', views.delete_violation, name='delete_violation'),
]