from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Category, Subscription, Record


# @shared_task
# def with_every_new_post(sender, instance, created, **kwargs):
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

new_record = Record.objects.all().exclude(time_in__gt=datetime.now() - timedelta(minutes=5))

@shared_task
def with_every_new_post(sender, instance, created, **kwargs):
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






@shared_task
def weekly_newsletter():

    for category in Category.objects.all():  # перебираем категории

        # получаем email подписчиков по категориям
        subscribers = list(Subscription.objects.filter(category=category).values_list('user__email', flat=True))
        # получаем публикации по категориям за последне 7 дней
        posts_list = list(category.record_set.filter(data__gte=datetime.utcnow() - timedelta(days=7)))

        if len(posts_list) == 0:  # если список публикаций пуст, то рассылка не выполняется.
            break

        for email in subscribers:

            html_content = render_to_string(
                'daily_post.html',
                {
                    'link': settings.SITE_URL,
                    'posts_list': posts_list,
                }
            )

            msg = EmailMultiAlternatives(
                subject='Статьи за неделю',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email], )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
