from django.db import models
from django.conf import settings

class Activity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('CP', 'Competitive Programming'),
        ('WS', 'Workshop'),
        ('HT', 'Hackathon'),
        ('CB', 'Coding Bootcamp'),
        ('OL', 'Online Activity'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    activity_type = models.CharField(max_length=2, choices=ACTIVITY_TYPE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    online_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='participants')
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity.name}"

class Result(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='results')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='result')
    rank = models.PositiveIntegerField()
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('activity', 'rank')  # Ensure no duplicate ranks for the same activity
        ordering = ['rank']

    def __str__(self):
        return f"{self.participant.user.username} - {self.activity.name} - Rank: {self.rank}"
