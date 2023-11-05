from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None):
        if not phone_number:
            raise ValueError("phone_number is required")
        if not name:
            raise ValueError("Username is required")
        user = self.model(phone_number=phone_number, name=name)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone_number, name, password=None):
        if not phone_number:
            raise ValueError("phone_number is required")
        if not name:
            raise ValueError("Username is required")
        user = self.create_user(phone_number=phone_number, name=name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255, unique=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True)
    username = None
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email