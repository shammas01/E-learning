from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email_live_confierm(user=None, email=None, message=None, subject=None):
    mail_subject=subject
    message = render_to_string(
        "emailforlive.html", {"user":user, "message":message, "email":email}
    )
    to_email = email

    send_mail = EmailMessage(mail_subject, message, email, to=[to_email])
    send_mail.send()