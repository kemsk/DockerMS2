from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class StudentData(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    student_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    course = models.CharField(max_length=200)
    year_level = models.CharField(max_length=10)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    card_expiry_date = models.DateField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    school_year = models.CharField(max_length=200, blank=True, null=True)
    college = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class AdminData(models.Model):
    admin_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=200, blank=True, null=True)
    emergency_contactname = models.CharField(max_length=200, blank=True, null=True)
    card_expiry_date = models.DateField(blank=True, null=True)


class PhotoUpload(models.Model):
    student = models.ForeignKey('StudentData', on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.student}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.email})"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


from rest_framework import serializers
from .models import StudentData, PhotoUpload

class StudentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentData
        fields = '__all__'


class PhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoUpload
        fields = ['id', 'title', 'image', 'uploaded_at', 'student']

    def validate_image(self, value):
        if not value.content_type in ['image/jpeg', 'image/jpg']:
            raise serializers.ValidationError("Only JPEG or JPG image files are allowed.")
        return value
