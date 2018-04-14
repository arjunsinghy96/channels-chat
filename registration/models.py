from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Password and email are required. Other fields are optional.
    """
    
    phone_no = models.CharField(max_length=13, null=True)
    avatar = models.ImageField(upload_to="avatars/")