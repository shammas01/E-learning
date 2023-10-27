from django.core.mail import EmailMessage

  
def send_email(subject, message, sender, recipient_list):
    email = EmailMessage(subject, message, sender, recipient_list)
    email.send()