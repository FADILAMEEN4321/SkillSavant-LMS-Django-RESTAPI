from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def send_enrollment_email(student_email, course_title):
    subject = 'Course Enrollment Successful'
    message = f'Thank you for enrolling in {course_title}.'
    from_email = 'your_email@example.com'
    recipient_list = [student_email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print('Email sent successfully.')
    except Exception as e:
        print(f'An error occurred while sending the email: {e}') 