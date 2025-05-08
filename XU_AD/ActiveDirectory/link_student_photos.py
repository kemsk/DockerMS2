import os
from ActiveDirectory.models import StudentDirectory
from django.conf import settings

# Script to link photos in media/student_photos to students by student_id (filename must match student_id)
def link_photos():
    photos_dir = os.path.join(settings.MEDIA_ROOT, 'student_photos')
    if not os.path.exists(photos_dir):
        print(f'Directory {photos_dir} does not exist.')
        return
    count = 0
    for filename in os.listdir(photos_dir):
        if filename.lower().endswith('.jpg'):
            student_id = os.path.splitext(filename)[0]
            try:
                student = StudentDirectory.objects.get(student_id=student_id)
                student.photo = f'student_photos/{filename}'
                student.save()
                count += 1
                print(f'Linked {filename} to student {student_id}')
            except StudentDirectory.DoesNotExist:
                print(f'No student found for ID {student_id}')
    print(f'Finished. {count} photos linked.')

# To use this script, run it in Django shell:
# from ActiveDirectory.link_student_photos import link_photos
# link_photos()
