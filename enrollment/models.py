from django.db import models
from course.models import Course, Module
from accounts.models import StudentProfile, InstructorProfile


class ModuleProgress(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def mark_as_completed(self):
        self.is_completed = True
        self.save()

    class Meta:
        unique_together = ["module", "student"]


class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def completion_percentage(self):
        modules_total = self.course.module_set.count()
        modules_completed = ModuleProgress.objects.filter(
            student = self.student,
            module__course=self.course,
            is_completed=True,
        ).count()

        if modules_total == 0:
            return 0

        percentage = (modules_completed / modules_total) * 100
        return round(percentage, 2)    



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
    payment_id = models.CharField(
        max_length=100, verbose_name="Payment ID", null=True, blank=True
    )
    order_id = models.CharField(
        max_length=100, verbose_name="Order ID", null=True, blank=True
    )
    signature = models.CharField(
        max_length=200, verbose_name="Signature", null=True, blank=True
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-transaction_date"]
