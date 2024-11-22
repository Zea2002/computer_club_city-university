from django.db import models
from user.models import User

# Position choices
POSITION_CHOICES = [
    ('President', 'President'),
    ('Vice President', 'Vice President'),
    ('General Secretary', 'General Secretary'),
    ('Treasurer', 'Treasurer'),
    ('PR Officer', 'PR Officer'),
    ('Technical Coordinator', 'Technical Coordinator'),
    ('Event Coordinator', 'Event Coordinator'),
    ('Creative Head', 'Creative Head'),
    ('Membership Coordinator', 'Membership Coordinator'),
    ('Training Head', 'Training Head'),
    ('Web Admin', 'Web Admin'),
    ('Social Media Manager', 'Social Media Manager'),
    ('Logistics Head', 'Logistics Head'),
    ('Outreach Coordinator', 'Outreach Coordinator'),
    ('Research Lead', 'Research Lead'),
    ('Alumni Coordinator', 'Alumni Coordinator'),
]

# Candidate Model
class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    manifesto = models.TextField(null=True)

    def __str__(self):
        return f"{self.user.username} ({self.position})"

# Vote Model
class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)

    class Meta:
        unique_together = ('voter', 'position')  # Prevent multiple votes per position

    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.user.username} ({self.position})"
