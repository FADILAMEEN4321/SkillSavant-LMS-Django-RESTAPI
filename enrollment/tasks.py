from celery import shared_task
from django.core.mail import send_mail
from enrollment.models import EnrolledCourse


@shared_task()
def send_enrollment_email(student_email, course_title):
    subject = "Course Enrollment Successful"
    message = f"Thank you for enrolling in {course_title}."
    from_email = "your_email@example.com"
    recipient_list = [student_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        print("Email sent successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")


@shared_task
def send_enrollment_emails_tasks():
    enrolled_courses = EnrolledCourse.objects.all()
    for enrolled_course in enrolled_courses:
        student_email = enrolled_course.student.user.formatted_student_email()
        course_title = enrolled_course.course.title

        subject = "Enrolled Course update."
        message = f"See your progress for {course_title}."
        from_email = "your_email@example.com"
        recipient_list = [student_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
