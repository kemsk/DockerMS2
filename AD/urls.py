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
    create_user_and_token,
    decode_jwt_token,
    get_admins,
    create_admin,
    update_admin,
    patch_admin,
    delete_admin,
    upload_photo,
)

urlpatterns = [
    # Student API
    path('api/students', get_students),                             # GET all
    path('api/students/<int:student_id>', get_students),            # GET one
    path('api/students/create', create_student),                    # POST
    path('api/students/update/<int:student_id>', update_student),   # PUT
    path('api/students/patch/<int:student_id>', patch_student),     # PATCH
    path('api/students/delete/<int:student_id>', delete_student),   # DELETE

    # Auth
    path('api/auth/create-user-token', create_user_and_token),
    path('api/auth/decode-token', decode_jwt_token),

    # Admin API
    path('api/admins', get_admins),
    path('api/admins/<int:admin_id>', get_admins),
    path('api/admins/create', create_admin),
    path('api/admins/<int:admin_id>/update', update_admin),
    path('api/admins/<int:admin_id>/patch', patch_admin),
    path('api/admins/<int:admin_id>/delete', delete_admin),

    #Photo upload
    path('api/upload-photo', upload_photo, name='upload-photo'),

    #Get photo 
    path('api/students/<int:student_id>/photos', get_photos_by_student, name='get-student-photos'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)