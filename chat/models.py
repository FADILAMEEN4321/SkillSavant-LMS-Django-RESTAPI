from django.db import models
from enrollment.models import Course
from accounts.models import CustomUser
from django.utils import timezone


class ChatMessage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.first_name} - {self.timestamp}"
