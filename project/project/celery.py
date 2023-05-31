import os                             # импортируем библиотеку для взаимодействия с операционной системой
from celery import Celery             # импортируем библиотеку Celery
from celery.schedules import crontab

# связываем настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')  # создаем экземпляр приложения Celery
# Устанавливаем для него файл конфигурации. Мы также указываем пространство имен, чтобы Celery сам находил все
# необходимые настройки в общем конфигурационном файле settings.py. Он их будет искать по шаблону «CELERY_***»
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()  # указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта

# отправлять уведомления каждый понедельник в 8 утра, о новых публикациях (подписчикам категорий)
app.conf.beat_schedule = {
    'send_notification_every_monday_8am': {
        'task': 'news.tasks.weekly_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

