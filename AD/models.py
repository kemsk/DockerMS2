from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class StudentData(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    course = models.CharField(max_length=200)
    yearlevel = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    contactnumber = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    emergencycontactnumber = models.CharField(max_length=200, blank=True, null=True)
    emergencycontactname = models.CharField(max_length=200, blank=True, null=True)
    cardexpirydate = models.DateField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    schoolyear = models.CharField(max_length=200, blank=True, null=True)
    college = models.CharField(max_length=200, blank=True, null=True)
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
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
