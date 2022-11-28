from celery import shared_task
from django.core.mail import send_mail
from codevance.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_email_task(user_email, email_subject, email_message):
    send_mail(
        subject=str(email_subject),
        message=str(email_message),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user_email]
        )
