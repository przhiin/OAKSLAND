from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    # Optional fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.username
