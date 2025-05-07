from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import get_photos_by_student
from .views import (
    get_students,
    create_student,
    update_student,
    patch_student,
    delete_student,
    create_user,
    decode_jwt_token,
    get_admins,
    login,
    update_admin,
    patch_admin,
    delete_admin,
    upload_photo,
)

urlpatterns = [
    # Student API
    path('api/students', get_students),                             
    path('api/students/<int:student_id>', get_students),           
 

    # Auth
    path('api/auth/create-user-token', create_user),
    path('api/auth/decode-token', decode_jwt_token),
    path('api/auth/login', login),

    # Admin API
    path('api/admins', get_admins),
    path('api/admins/<int:admin_id>', get_admins),
    path('api/admins/<int:admin_id>/update', update_admin),
    path('api/admins/<int:admin_id>/patch', patch_admin),
    path('api/admins/<int:admin_id>/delete', delete_admin),
    path('api/admins/students/create', create_student),                    
    path('api/admins/students/update/<int:student_id>', update_student),   
    path('api/admins/students/patch/<int:student_id>', patch_student),     
    path('api/admins/students/delete/<int:student_id>', delete_student), 

    #Photo upload
    path('api/upload-photo', upload_photo, name='upload-photo'),

    #Get photo 
    path('api/students/<int:student_id>/photos', get_photos_by_student, name='get-student-photos'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)