from django.urls import path
from . import views

app_name = 'ts.personel'

urlpatterns = [
    path('dashboard', views.dashboard_view, name='Dashboard'),
    path('create-ticket', views.add_ticket, name="CreateTicket"),
    path('ticket/<int:ticket_id>/ticket-details', views.ticket_details_view, name="TicketDetails"),
    path('ticket/<int:ticket_id>/update/id-status', views.update_id_status, name="IDStatus"),
]
