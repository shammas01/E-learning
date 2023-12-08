from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import LiveClassDetailsModel, liveEnroll
from pytz import timezone

@shared_task(bind=True)
def send_email_reminder(self, live_session_id):
    live_session = LiveClassDetailsModel.objects.get(id=live_session_id)
    enrolled_user = liveEnroll.objects.filter(lives=live_session).first()

    utc_time = live_session.class_start_datetime.replace(tzinfo=timezone('UTC'))
    asia_kolkata_time = utc_time.astimezone(timezone('Asia/Kolkata'))
    
    if enrolled_user:
        user = enrolled_user.user
        mail_subject = f"Reminder: Your live session '{live_session.title}' is starting soon!"
        message = f"Your session starts at {asia_kolkata_time.strftime('%Y-%m-%d %H:%M')}"
        to_email = user.email
        
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "you live mail is shedulled successfully"

        