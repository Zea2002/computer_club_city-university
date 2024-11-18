from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    batch = models.CharField(max_length=100, null=True, blank=True)  # Add batch field

    def __str__(self):
        return self.username
