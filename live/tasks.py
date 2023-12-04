from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from useraccount.models import User

@shared_task(bind=True)
def fun(self):
    # operations
    print("You are in Fun function")
    return "done"


@shared_task(bind=True)
def send_mail_func(self):
    users=User.objects.all()
    for user in users:
        mail_subject="hello celery"
        message="subscribe TheCodeSpace Youtube channel."
        to_email=user.email
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
            )
    return "Task Successfull"