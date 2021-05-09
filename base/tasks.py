from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject,html_message,plain_message,
				from_email,to):
	t=send_mail(subject, plain_message, from_email,to,html_message=html_message)
	return 'invoice has being send Successfully to email'


@shared_task
def mul(x, y):
    return x * y
