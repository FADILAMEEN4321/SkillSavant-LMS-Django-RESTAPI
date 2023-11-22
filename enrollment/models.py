from django.db import models
from course.models import Course
from accounts.models import StudentProfile,InstructorProfile



class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    module_completion_status = models.JSONField(default=dict, null=True, blank=True)



class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)



class Transcation(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    instructor_share = models.DecimalField(max_digits=15, decimal_places=2)
    company_share = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID", null=True, blank=True)
    order_id = models.CharField(max_length=100, verbose_name="Order ID", null=True, blank=True)
    signature = models.CharField(max_length=200, verbose_name="Signature", null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['-transaction_date']


