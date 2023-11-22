from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    ROLES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','role']
    role = models.CharField(max_length=10, choices=ROLES, default='student')
    is_blocked = models.BooleanField(default=False, blank=True, null=True)
    phone_number = models.CharField(max_length=30, unique=True, blank=True, null=True)



class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.FileField(upload_to='student_profiles/',blank=True, null=True)

    def __str__(self):
        return self.user.email 
    


class InstructorProfile(models.Model):
     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
     bio = models.TextField(blank=True, null=True)
     skill = models.CharField(max_length=50, blank=True, null=True)
     profile_photo = models.FileField(upload_to='instructor_profiles/',blank=True, null=True)
     wallet = models.DecimalField(max_digits=15, decimal_places=2, default=0)

     def __str__(self):
        return self.user.email
     


class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_photo = models.FileField(upload_to='admin_profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.email



