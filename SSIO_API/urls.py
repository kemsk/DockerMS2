from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('get-data/<int:ticket_id>', views.get_ticket, name="TicketData"),
    path('change-active', views.active_year),
    path('check-acad-year/<int:acad_year_id>', views.acad_year_checker),
    path('<int:ticket_id>/update-status', views.update_status)
]