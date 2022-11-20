import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'mailing_every_monday': {
        'task': 'news.tasks.weekly_announcement',
        'schedule': crontab(hour=1, minute=1, day_of_week=1),
        'args': (),
    },
}

app.autodiscover_tasks()