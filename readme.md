# XUSSIO Active Directory #

## Working Endpoints ##

Student API
api/students                            
api/students/<int:student_id>         
api/students/create                   
api/students/update/<int:student_id>/ 
api/students/patch/<int:student_id>/ 
api/students/delete/<int:student_id>/

Auth
api/auth/create-user-token
api/auth/decode-token

Admin API
api/admins
api/admins/<int:admin_id>
api/admins/create
api/admins/<int:admin_id>/update
api/admins/<int:admin_id>/patch
api/admins/<int:admin_id>/delete

Photo upload
api/upload-photo

Get photo 
api/students/<int:student_id>/photos
