from django.db import models
from user.models import User

class Executive(models.Model):
    DESIGNATION_CHOICES = [
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('General Secretary', 'General Secretary'),
        ('Treasurer', 'Treasurer'),
        ('PR Officer', 'Public Relations Officer'),
        ('Technical Coordinator', 'Technical Coordinator'),
        ('Event Coordinator', 'Event Coordinator'),
        ('Creative Head', 'Creative Head'),
        ('Membership Coordinator', 'Membership Coordinator'),
        ('Training Head', 'Training and Development Head'),
        ('Web Admin', 'Web Administrator'),
        ('Social Media Manager', 'Social Media Manager'),
        ('Logistics Head', 'Logistics Head'),
        ('Outreach Coordinator', 'Outreach Coordinator'),
        ('Research Lead', 'Research and Innovation Lead'),
        ('Alumni Coordinator', 'Alumni Coordinator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    description = models.TextField(blank=True, null=True)
    linkedIn = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.designation})"
