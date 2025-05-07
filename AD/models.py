from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# ----------------- STUDENT DATA -----------------
class StudentData(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
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

# ----------------- ADMIN DATA -----------------
class AdminData(models.Model):
    admin_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)  # fixed typo
    card_expiry_date = models.DateField(blank=True, null=True)

# ----------------- PHOTO UPLOAD -----------------
class PhotoUpload(models.Model):
    student = models.ForeignKey('StudentData', on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.student}"

# ----------------- USER MODEL -----------------
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='personnel'):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        if role not in ['admin', 'personnel']:
            raise ValueError('Role must be either "admin" or "personnel"')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('personnel', 'Personnel')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Needed for Django admin

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.role})"
