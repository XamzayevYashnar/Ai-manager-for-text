from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here. 

class MainUser(AbstractUser):
    avatar = models.ImageField(upload_to="users_pictures", null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='mainuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='mainuser_permissions_set', 
        blank=True,
    )