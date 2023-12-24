from django.db import models
from accounts.models import InstructorProfile, StudentProfile
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="Beginner")
    is_approved = models.BooleanField(default=False)
    unlisted = models.BooleanField(default=False)
    cover_image = models.FileField(upload_to="course_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_duration(self):
        total_duration = timedelta()

        for module in self.module_set.all():
            total_duration += module.duration

        # Calculate hours, minutes, and seconds
        hours, remainder = divmod(total_duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the result
        formatted_duration = "{:02}:{:02}:{:02}".format(
            int(hours), int(minutes), int(seconds)
        )
        return formatted_duration

    def formatted_created_at(self):
        return self.created_at.strftime("%d-%m-%Y")

    class Meta:
        ordering = ["created_at"]


class Module(models.Model):
    module_title = models.CharField(max_length=100)
    duration = models.DurationField(default=timedelta(), null=True, blank=True)
    module_order = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    transcript = models.TextField(null=True, blank=True)
    video_url = models.FileField(upload_to="module_videos/")
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    notes = models.FileField(upload_to="module_notes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.module_title

    class Meta:
        ordering = ["module_order"]


class FavouriteCourses(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now=True)
