from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Record
from .tasks import *

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender=Record)  # декоратор для сигналов
def record_created(sender, instance, created, **kwargs):
    """Сигнал срабатывает при появлении новой публикации и вызывает таску"""
    if created:  # при появлении новой публикации
        # получаем email подписчиков этой публикации
        emails = list(User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True))

        # вызываем нашу таску и передаем ей необходимые аргументы
        with_every_new_post.delay(instance.category.title,
                                  instance.preview(),
                                  instance.title,
                                  emails,
                                  instance.get_absolute_url(),
                                  )


# ф-я выполнятся при создании объекта модели Record
# @receiver(post_save, sender=Record)  # декоратор для сигналов
# def record_created(sender, instance, created, **kwargs):
#     """Сигнал срабатывает при появлении новой публикации и выполняет рассылку всем подписчикам категории"""
#     if created:
#         emails = User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True)
#
#         subject = f'Новая запись в категории {instance.category}'
#
#         text_content = (
#             f'Название: {instance.title}\n'
#             f'Анонс: {instance.preview()}\n\n'
#             f'Ссылка на публикацию: {settings.SITE_URL}{instance.get_absolute_url()}'
#         )
#         html_content = (
#             f'Название: {instance.title}<br>'
#             f'Анонс: {instance.preview()}<br><br>'
#             f'<a href="{settings.SITE_URL}{instance.get_absolute_url()}">'
#             f'Ссылка на публикацию</a>'
#         )
#         for email in emails:
#             msg = EmailMultiAlternatives(subject, text_content, None, [email])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
