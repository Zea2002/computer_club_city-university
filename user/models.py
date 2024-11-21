from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail

class User(AbstractUser):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    batch = models.CharField(max_length=100, null=True, blank=True)  # Add batch field
    student_id=models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name} "
    
    
    def send_approval_email(self):
            if self.status == 'Approved':
                send_mail(
                    'Membership Approval',
                    f'Hi {self.username},\n\nYour membership has been approved. Welcome to our community!',
                    'admin@yourdomain.com',  
                    [self.email],
                    fail_silently=False,
                )