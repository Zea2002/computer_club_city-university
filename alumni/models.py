from django.db import models
from user.models import User

# Create your models here.
class Alumni(models.Model):
    name=models.CharField(max_length=100 ,default=None)
    image=models.ImageField(upload_to='alumni_images/', blank=True, null=True)
    graduation_year = models.PositiveIntegerField() 
    department = models.CharField(max_length=100, blank=True, null=True)  
    job_title = models.CharField(max_length=100, blank=True, null=True)  
    company = models.CharField(max_length=100, blank=True, null=True)  
    linkedin_profile = models.URLField(blank=True, null=True)  
    bio = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name