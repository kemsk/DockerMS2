from django.urls import path
from . import views



urlpatterns = [
    path('api/students', views.get_students),                        # GET all
    path('api/students/<int:student_id>', views.get_students),       # GET one
    path('api/students/create', views.create_student),               # POST
    path('api/students/update/<int:student_id>', views.update_student),  # PUT
    path('api/students/patch/<int:student_id>', views.patch_student),   # PATCH
    path('api/students/delete/<int:student_id>', views.delete_student), # DELETE
    path('api/auth/create-user-token', views.create_user_and_token), #for token
    path('api/auth/decode-token', views.decode_jwt_token),
]
