from django.core.mail import send_mail
from advertisingSystem.settings import EMAIL_HOST_USER

def sendMail(advertise, message):
    send_mail(
        subject='Advertise status',
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[advertise.email]
    )