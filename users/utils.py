import re
import threading
from rest_framework.validators import ValidationError
from django.core.mail import send_mail
from django.core.mail import send_mail

email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
phone_regex = re.compile(r"^\+?[0-9]{9,15}$")
username_regex = re.compile(r"^[a-zA-Z0-9_]{3,16}$")


def check_email_or_phone_number(email_phone_number):
    if re.fullmatch(email_regex, email_phone_number):
        email_phone_number = "email"
    elif re.fullmatch(phone_regex, email_phone_number):
        email_phone_number = "phone_number"
    else:
        raise ValidationError({"msg": "Invalid email or phone number"})

    return email_phone_number


def check_user_input(user_input):
    if re.fullmatch(email_regex, user_input):
        user_input = "email"
    elif re.fullmatch(phone_regex, user_input):
        user_input = "phone_number"
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"
    else:
        raise ValidationError({"msg": "Invalid email or phone number"})

    return user_input


def send_code_to_email(email, code):
    def send():
        message = f"Your code is {code}"
        send_mail(
            subject="Register code",
            message=message,
            from_email="abdukodirarifzanov@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

    thread = threading.Thread(target=send)
    thread.start()
    return thread
