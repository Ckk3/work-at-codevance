from celery import shared_task
from django.core.mail import send_mail
from time import sleep
from codevance.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_email_task(user_email, subject, message):
    send_mail(
        subject=subject, 
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user_email]
        )
