from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Avatar', null=True, blank=True)
    phone = models.CharField(max_length=35, verbose_name='Phone', null=True, blank=True)
    country = models.CharField(max_length=50, verbose_name='Country', null=True, blank=True)
    
    token = models.CharField(max_length=100, verbose_name='Token', null=True, blank=True)
    is_manager = models.BooleanField(default=False, verbose_name='Manager Role')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
