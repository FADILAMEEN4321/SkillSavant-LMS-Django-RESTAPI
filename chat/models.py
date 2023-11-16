from django.db import models
from enrollment.models import EnrolledCourse
from accounts.models import CustomUser
from django.utils import timezone

class ChatMessage(models.Model):
    course = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} - {self.timestamp}"
