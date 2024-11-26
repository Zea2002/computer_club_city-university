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

# Candidate model
class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manifesto = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position}"

    # Update the vote count for the candidate
    def update_vote_count(self):
        self.votes = Vote.objects.filter(candidate=self).count()
        self.save()


# Vote model
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'position')  # One vote per position per user

    def __str__(self):
        return f"{self.user.first_name} voted for {self.candidate.position}"

    # Override the save method to update the candidate's vote count
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update vote count for the candidate after saving the vote
        self.candidate.update_vote_count()
