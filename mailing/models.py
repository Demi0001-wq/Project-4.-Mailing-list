from django.db import models
from django.conf import settings

NULLABLE = {'null': True, 'blank': True}

class Recipient(models.Model):
    email = models.EmailField(verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='Full Name')
    comment = models.TextField(verbose_name='Comment', **NULLABLE)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', **NULLABLE)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = 'Recipient'
        verbose_name_plural = 'Recipients'


class Message(models.Model):
    subject = models.CharField(max_length=200, verbose_name='Subject')
    body = models.TextField(verbose_name='Body')
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Mailing(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Start Time')
    end_time = models.DateTimeField(verbose_name='End Time', **NULLABLE)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, verbose_name='Period')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name='Status')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Message')
    recipients = models.ManyToManyField(Recipient, verbose_name='Recipients')
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Owner', **NULLABLE)

    def __str__(self):
        return f"Mailing {self.id} ({self.status})"

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'


class MailingLog(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failure', 'Не успешно'),
    ]

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Last Try')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Status')
    server_response = models.TextField(verbose_name='Server Response', **NULLABLE)

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Mailing')

    def __str__(self):
        return f"Log {self.id} for {self.mailing}"

    class Meta:
        verbose_name = 'Mailing Log'
        verbose_name_plural = 'Mailing Logs'
