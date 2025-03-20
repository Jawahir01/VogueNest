from django.db import models
from django.utils import timezone

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission from {self.name} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"