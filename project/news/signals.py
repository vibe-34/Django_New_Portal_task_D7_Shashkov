from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from .models import Record

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


# ф-я выполняться при создании объекта модели Record
@receiver(post_save, sender=Record)  # декоратор для сигналов
def record_created(sender, instance, created, **kwargs):
    if created:
        emails = User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True)

        subject = f'Новая запись в категории {instance.category}'

        text_content = (
            f'Название: {instance.title}\n'
            f'Анонс: {instance.preview()}\n\n'
            f'Ссылка на публикацию: {settings.SITE_URL}{instance.get_absolute_url()}'
        )
        html_content = (
            f'Название: {instance.title}<br>'
            f'Анонс: {instance.preview()}<br><br>'
            f'<a href="{settings.SITE_URL}{instance.get_absolute_url()}">'
            f'Ссылка на публикацию</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
