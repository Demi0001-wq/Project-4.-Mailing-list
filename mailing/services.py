from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingLog
from django.utils import timezone

def send_mailing(mailing):
    """
    Sends the mailing to all its recipients and logs the result.
    """
    try:
        recipient_list = [recipient.email for recipient in mailing.recipients.all()]
        
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        
        MailingLog.objects.create(
            status='success',
            server_response='Email sent successfully',
            mailing=mailing
        )
        
        if mailing.status == 'created':
            mailing.status = 'started'
            mailing.save()
            
    except Exception as e:
        MailingLog.objects.create(
            status='failure',
            server_response=str(e),
            mailing=mailing
        )

def run_mailings():
    """
    Checks all mailings and sends those that should be sent based on their schedule.
    """
    now = timezone.now()
    mailings_to_run = Mailing.objects.filter(
        start_time__lte=now,
        status__in=['created', 'started']
    )
    
    for mailing in mailings_to_run:
        # Simplified logic: 
        # In a real app, you'd check the last log entry to see if 
        # it's time to send again based on the period (daily, weekly, etc.)
        send_mailing(mailing)
