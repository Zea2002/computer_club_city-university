from django.db import models

# Create your models here.
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

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    photo = models.ImageField(upload_to='executives/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.designation})"