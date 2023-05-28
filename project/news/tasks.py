from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import Category, Subscription, Record


# @shared_task
# def with_every_new_post(pk):  # В задачу передаем pk новой статьи
#     record = Record.objects.get(pk=pk)  # Получаем публикацию по полученному pk
#     categories = record.post_category.all()  # определяем все категорию у этого поста ???
#     title = record.post_title  # получаем заголовок публикации
#     subscribers_emails = []  # создаем пустой список подписчиков
#     for categpry in categories:  # проходимся по всем категориям этого поста???
#         subscribers_email = category.subscribers.all()  # получаем всех подписчиков у этой категории
#         for sub_user in subscribers_email:  # проходимся по всем подписчикам этой категории
#             subscribers_emails.append(sub_user.email)  # на каждой итерации забираем емайл и кладем его в пустой список


    # здесь нужно выполнить рассылку

@shared_task
def with_every_new_post(preview, pk, title, emails, instance):

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

# @shared_task
# def with_every_new_post(preview, pk, title, subscribers):                                                                    # отдельно делаем функцию отправки сообщения о новом посте для подписчика
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/post/{pk}'  # http://127.0.0.1:8000/post/pk
#         }
#     )
#     msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()





# @shared_task
# def with_every_new_post():
#
#     for category in Category.objects.all():  # перебираем категории
#
#         # получаем email подписчиков по категориям
#         subscribers = list(Subscription.objects.filter(category=category).values_list('user__email', flat=True))
#         # получаем публикации по категориям за последне 7 дней
#         posts_list = list(category.record_set.filter(data__gte=datetime.utcnow() - timedelta(minutes=1)))
#
#         if len(posts_list) == 0:  # Если список публикаций пуст, то рассылка не выполняется
#             break
#
#         for email in subscribers:
#
#             html_content = render_to_string(
#                 'daily_post.html',
#                 {
#                     'link': settings.SITE_URL,
#                     'posts_list': posts_list,
#                 }
#             )
#
#             msg = EmailMultiAlternatives(
#                 subject='Статьи за неделю',
#                 body='',
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[email], )
#             msg.attach_alternative(html_content, 'text/html')
#             msg.send()
#
#
# @shared_task
# def weekly_newsletter():
#
#     for category in Category.objects.all():  # перебираем категории
#
#         # получаем email подписчиков по категориям
#         subscribers = list(Subscription.objects.filter(category=category).values_list('user__email', flat=True))
#         # получаем публикации по категориям за последне 7 дней
#         posts_list = list(category.record_set.filter(data__gte=datetime.utcnow() - timedelta(days=7)))
#
#         if len(posts_list) == 0:  # Если список публикаций пуст, то рассылка не выполняется
#             break
#
#         for email in subscribers:
#
#             html_content = render_to_string(
#                 'daily_post.html',
#                 {
#                     'link': settings.SITE_URL,
#                     'posts_list': posts_list,
#                 }
#             )
#
#             msg = EmailMultiAlternatives(
#                 subject='Статьи за неделю',
#                 body='',
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[email], )
#             msg.attach_alternative(html_content, 'text/html')
#             msg.send()
