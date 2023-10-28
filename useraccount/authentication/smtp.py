from django.core.mail import EmailMessage
from django.template.loader import render_to_string

  
# def send_email(subject=None, message=None, to_mail=None):
#     to_mail = to_mail
#     email = EmailMessage(subject, message,to=[to_mail] )
#     email.send()

def send_email(user=None, email=None, message=None, otp=None, subject=None):
    mail_subject = subject
    message = render_to_string("email.html", {
        'user': user,
        'otp':otp,
        'message':message,
        'email':email
    })
    to_email = email
    
    send_mail = EmailMessage(mail_subject, message, email, to=[to_email])
    send_mail.send()