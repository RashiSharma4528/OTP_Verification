import random

from django.core.mail import send_mail

from django.conf import settings

def generate_otp():
    return str(random.randint(100000,999999))

def send_otp_email(email, otp):

    subject = "OTP Verification"

    message = f"""
Hello,

Your OTP is:

{otp}

It is valid for 5 minutes.

Do not share this OTP with anyone.
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )