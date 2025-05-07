from rest_framework import serializers
from .models import PhotoUpload, StudentData

class PhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoUpload
        fields = ['id', 'title', 'image', 'uploaded_at', 'student']

    def validate_image(self, value):
        valid_extensions = ['.jpeg', '.jpg']
        if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError("Only .jpeg or .jpg files are allowed.")
        return value
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = ['student_id', 'first_name', 'last_name']
