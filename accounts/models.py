from datetime import timezone
from email.policy import default
from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager
from django.contrib.auth.models import User

import uuid

# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):

    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=12,unique=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    blocked=models.BooleanField(default=False)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','phone']
    objects=CustomUserManager()


    def __str__(self):
        return self.first_name


