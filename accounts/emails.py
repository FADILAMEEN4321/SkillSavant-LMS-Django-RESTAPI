from django.core.mail import send_mail
import random
from .models import CustomUser
from django.conf import settings

def send_otp_via_email(email):
    subject = "Your account verification email"
    otp = random.randint(1000, 9999)
    message = f'Your otp is {otp}'
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list = [email],
        fail_silently=True,
    )

    user = CustomUser.objects.filter(email='student-' + email).first()
    print(user,'-----user')
    user.otp = otp
    user.save()
    print(user,'-----user')