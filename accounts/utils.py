import random
import requests
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = "OTP Verification"

    message = f"""
Hello,

Your OTP is:

{otp}

It is valid for 5 minutes.

Do not share this OTP with anyone.
"""

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {"email": settings.BREVO_SENDER_EMAIL, "name": "OTP Verification"},
        "to": [{"email": email}],
        "subject": subject,
        "textContent": message,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()