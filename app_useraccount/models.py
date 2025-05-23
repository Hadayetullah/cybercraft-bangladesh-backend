import uuid

from django.utils import timezone
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('You have not specified a valid email address')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    avater = models.ImageField(upload_to='uploads/avaters', null=True, blank=True)

    # OTP fields
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    # Status flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]


    # def otp_is_valid(self):
    #     """Checks if the OTP is valid and not expired."""
    #     if self.otp and self.otp_created_at:
    #         return timezone.now() < self.otp_created_at + timedelta(minutes=5)
    #     return False
    

    # def avater_url(self):
    #     if self.avater:
    #         return f'{settings.WEBSITE_URL}{self.avater.url}'
    #     else:
    #         return ''
        
    def __str__(self):
        return self.name
    
