from django.db import models

# Create your models here.


class Mentor(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    expertise = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='mentors/photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    linkedIn_id=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name
